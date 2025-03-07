import subprocess
import contractions
import spacy
import platform
import requests
import re
import math
import operator as op
import datetime
import pytz
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from deep_translator import GoogleTranslator

# 下載 NLTK 必需的資料
nlp = spacy.load("en_core_web_sm")

last_joke_requested = False
last_translation = None
last_definition = None
last_translation_lang = None

operators = {
    "+" : op.add,
    "-" : op.sub,
    "*" : op.mul,
    "/" : op.truediv,
    "**" : op.pow
}
math_functions = {
    "sin" : math.sin,
    "cos" : math.cos,
    "tan" : math.tan,
    "sqrt" : math.sqrt,
    "log" : math.log,
    "log10" : math.log10,
    "exp" : math.exp
}

def preprocess_text(text):
    text = contractions.fix(text)
    doc = nlp(text.lower())

    tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]
    return tokens

def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            # 正確的 JSON 解析路徑
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            return f"Definition of '{word}': {definition}"
        except (KeyError, IndexError) as e:
            # 如果 JSON 結構不匹配或缺少字段
            return f"Sorry, I couldn't find the definition of the word '{word}'."
    else:
        # 如果 API 請求失敗
        return f"Sorry, I couldn't find the definition of the word '{word}'."
    
def translate_text(text, target_language):
    try:
        if not text.strip():
            return "Please provide text to translate."
        
        language_map = {
            "chinese" : "zh-CN",
            "english" : "en",
            "french" : "fr",
            "german" : "de",
            "italian" : "it",
            "japanese" : "ja",
            "korean" : "ko",
            "spanish" : "es"
        }
        target_language = language_map.get(target_language.lower(), target_language)
        translated = GoogleTranslator(source='auto', target=target_language).translate(text)
        if translated:
            return f"{translated}"
        else:
            return "Translation failed. Please try again."
    except Exception as e:
        return f"An error occurred during translation: {str(e)}"

def get_time_info(user_input):
    now = datetime.datetime.now()

    if 'time' in user_input.lower():
        return f"The current time is {now.strftime('%H:%M:%S')}."
    if 'date' in user_input.lower():
        return f"Today's date is {now.strftime('%Y-%m-%d')}."
    
    date_match = re.search(r"how many days until (\w+)", user_input.lower())
    if date_match:
        event = date_match.group(1).strip().lower()
        event_dates = {
            "christmas" : datetime.date(now.year, 12, 25),
            "new year" : datetime.date(now.year + 1, 1, 1),
            "valentine's day" : datetime.date(now.year, 2, 14),
            "halloween" : datetime.date(now.year, 10, 31)
        }
        if event in event_dates:
            days_until = (event_dates[event] - now.date()).days
            return f"There are {days_until} days until {event}."
        return "I'm not clear about the event you typed. Please try other events such as 'christmas' or 'new year'."
    
    timeZone_match = re.search(r"time in (\w+)", user_input.lower())
    if timeZone_match:
        city = timeZone_match.group(1).strip().lower()
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        
        # 增加檢查 location 是否為 None
        if location:
            latitude = location.latitude
            longitude = location.longitude
            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
            print(f"Timezone found: {timezone_str}")  # 確認 timezone_str 是否有效
            
            if timezone_str:
                timezone = pytz.timezone(timezone_str)
                local_time = datetime.datetime.now(timezone)
                return f"The current time in {city} is {local_time.strftime('%H:%M:%S')}."
            else:
                print("Timezone could not be determined.")
        else:
            print(f"Location for {city} could not be found.")
        return f"I'm not clear about the city you typed. Please try other cities such as 'new york' or 'london'."

    return "I'm not sure what you are asking about."

def check_for_app_command(user_input):
    doc = nlp(user_input.lower())
    for token in doc:
        if token.pos_ == 'NOUN' and token.text in ['calculator', 'notepad']:  # ✅ 修正
            return token.text
    return None

def open_app(app_name):
    system = platform.system()
    
    if system == "Windows":
        if app_name == "calculator":
            subprocess.run(["calc"], shell=True)
        elif app_name == "notepad":
            subprocess.run(["notepad"], shell=True)
    elif system == "Darwin":  # macOS
        if app_name == "calculator":
            subprocess.run(["open", "-a", "Calculator"])
        elif app_name == "notepad":
            subprocess.run(["open", "-a", "TextEdit"])
    elif system == "Linux":
        if app_name == "calculator":
            subprocess.run(["gnome-calculator"])
        elif app_name == "notepad":
            subprocess.run(["gedit"])
    else:
        print(f"Unsupported OS: {system}")

def calculate_expression(expression):
    try:
        expression = expression.replace(" ", "")  # 去掉所有空格

        # 將百分比轉換為小數
        expression = re.sub(r'(\d+)%', lambda m: str(float(m.group(1)) / 100), expression)
        
        # 將 "of" 轉換為 "*"
        expression = expression.replace("of", "*")
        
        if not re.match(r'^[\d+\-*/().% sqrt sincostanlog]+$', expression):
            return "Invalid expression. Please enter a valid mathematical expression."

        # 使用 eval 進行計算
        result = eval(expression, {"__builtins__": None}, {**operators, **math_functions})
        return f"The result is: {result}"
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Error calculating expression: {str(e)}"

def get_joke():
    try:
        url = "https://api.chucknorris.io/jokes/random"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["value"]
        else:
            return "I didn't have any jokes at this moment.Let me think a bit..."
    except Exception as e:
        return "An error occurred while fetching a joke."
    
def get_weather(city):
    api_key = "5dac3b051c407fc1fcc3b4d8e6043446"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature_kelvin = data["main"]["temp"]
            temperature_celsius = temperature_kelvin - 273.15
            weather_description = data["weather"][0]["description"]
            return f"The temperature in {city} is {weather_description} with a temperature of {temperature_celsius:.1f}°C."
        else:
            return "Are you sure you living in earth?"
    except  Exception as e:
        return "An error occurred while fetching weather data."

def generate_response(user_input):
    global last_joke_requested, last_translation, last_definition, last_translation_lang
    try:
        time_response = get_time_info(user_input)
        if time_response:
            return time_response

        how_about_match = re.search(r"how about (.+)", user_input.lower())
        if how_about_match:
            new_query = how_about_match.group(1).strip()
            if last_translation is not None:
                return translate_text(new_query, last_translation_lang)
            if last_definition is not None:
                return get_definition(new_query)
            return "Could you clarify what you mean by 'how about'?"
        define_match = re.search(r"define\s+(\w+)", user_input.lower())
        if define_match:
            word = define_match.group(1)
            last_definition = word
            return get_definition(word)

        if "translate" in user_input.lower() and "to" in user_input.lower():
            match = re.search(r"translate (.+?) to (\w+)", user_input.lower())
            if match:
                text, lang = match.groups()
                if text.strip() and lang.strip():
                    last_translation = text.strip()
                    last_translation_lang = lang.strip()
                    return translate_text(text.strip(), lang.strip())
                else:
                    "Please provide both text and target language."
            else:
                return "Please use the format: translate [your text] to [desired language]."
        
        app_command = check_for_app_command(user_input)
        if app_command:
            open_app(app_command)
            return f"Opening {app_command}..."

        if any(char in user_input for char in "0123456789+-*/^%") or \
            any(func in user_input.lower() for func in ["sqrt", "sin", "cos", "tan", "log"]):
            # 移除非數學相關的詞語
            expression = re.sub(r'[^0-9+\-*/().% of]', '', user_input)
            expression = expression.replace("of", "*")  # 將 "of" 轉換為 "*"
            if expression:
                return calculate_expression(expression)
            else:
                return "Please provide a valid mathematical expression."
        
        weather_keyword =  ["weather", "temperature"]
        if any(keyword in user_input.lower() for keyword in weather_keyword):
            doc = nlp(user_input.lower())
            cities = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
            if cities:
                city = cities[0]
                weather_info = get_weather(city)
                return weather_info
            else:
                return "Please provide a city name."
        
        next_joke_keywords = ["next", "next joke"]
        if last_joke_requested and any(keyword in  user_input.lower() for keyword in next_joke_keywords):
            return get_joke()
        joke_keywords = ["joke", "funny", "tell me a joke"]
        if any(keyword in user_input.lower() for keyword in joke_keywords):
            last_joke_requested = True
            return get_joke()
        last_joke_requested = False

        tokens = preprocess_text(user_input)
        user_sentences = " ".join(tokens)

        greetings = ["hello", "hi", "hey"]
        farewells = ["goodbye", "bye", "see you later"]
        help_intents = ["help", "what can you do"]
        favorites = ["favourite", "love", "like"]

        if any(greeting in user_sentences for greeting in greetings):
            return "Hello! How can I assist you today?"
        elif any(farewell in user_input.lower() for farewell in farewells):
            return "Goodbye! Have a nice day!"
        elif any(help_intent in user_input.lower() for help_intent in help_intents):
            return "I can chat with you in simple conversations. You can ask me anything!"
        elif any(favourite in user_sentences for favourite in favorites):
            return "I like to chat with you!"
        return "I'm not sure how to respond to that."
    
    except Exception as e:
        import traceback
        print(f"Error in generate_response: {e}")
        traceback.print_exc()
        return "Sorry, an error occurred while processing your request."
