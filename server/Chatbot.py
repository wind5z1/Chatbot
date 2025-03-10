import subprocess
import json
import contractions
import spacy
import platform
import requests
import re
import math
import operator as op
import datetime
import pytz
from deep_translator import GoogleTranslator

# 下載 NLTK 必需的資料
nlp = spacy.load("en_core_web_sm")

context_memory = {
    "last_joke_requested" : False,
    "last_translation" : None,
    "last_definition" : None,
    "last_translation_lang" : None,
    "user_name" : None
}
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

def save_context():
    with open("context_memory.json", "w") as f:
        json.dump(context_memory, f)
def load_context():
    global context_memory
    try:
        with open("context_memory.json", "r") as f:
            context_memory =json.load(f)
    except FileNotFoundError:
        pass 
load_context()   

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
    doc = nlp(user_input.lower())

    # 檢查是否提到 "time" 或 "date"
    if "time" in user_input.lower() or "date" in user_input.lower():
        # 嘗試從句子中找出地點（GPE = 地理位置實體）
        locations = [ent.text.lower() for ent in doc.ents if ent.label_ == "GPE"]

        # 城市對應的時區
        timezone_map = {
            "new york": "America/New_York",
            "london": "Europe/London",
            "paris": "Europe/Paris",
            "tokyo": "Asia/Tokyo",
            "beijing": "Asia/Shanghai",
            "hong kong": "Asia/Hong_Kong",
            "taipei": "Asia/Taipei",
            "sydney": "Australia/Sydney",
            "los angeles": "America/Los_Angeles",
            "malaysia": "Asia/Kuala_Lumpur",
            "singapore": "Asia/Singapore",
            "korea": "Asia/Seoul"
        }

        # 國家對應的主要城市
        country_timezone_map = {
            "japan": "tokyo",
            "china": "beijing",
            "usa": "new york",
            "america": "new york",
            "australia": "sydney",
            "uk": "london",
            "united kingdom": "london",
            "france": "paris",
            "taiwan": "taipei",
            "singapore": "singapore",
            "malaysia": "malaysia",
            "korea": "korea"
        }

        if locations:
            location = locations[0]

            # 如果輸入的是國家名稱，轉換為城市名稱
            if location in country_timezone_map:
                location = country_timezone_map[location]

            # 檢查城市是否在時區對應表內
            if location in timezone_map:
                tz = pytz.timezone(timezone_map[location])
                now = datetime.datetime.now(tz)
                if "time" in user_input.lower():
                    return f"The current time in {location.title()} is {now.strftime('%H:%M:%S')}."
                elif "date" in user_input.lower():
                    return f"The current date in {location.title()} is {now.strftime('%Y-%m-%d')}."
            else:
                return "Sorry, I don't know the timezone for that location. Please try another city."
        
        # 如果沒有提供地點，就返回 UTC 時間
        now = datetime.datetime.utcnow()
        if "time" in user_input.lower():
            return f"The current UTC time is {now.strftime('%H:%M:%S')}."
        elif "date" in user_input.lower():
            return f"The current UTC date is {now.strftime('%Y-%m-%d')}."
    
    return None  # 如果沒有符合的條件，返回 None
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
    
def get_weather(city, day_offset):
    api_key = "5dac3b051c407fc1fcc3b4d8e6043446"
    if day_offset == 0:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    else:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if day_offset == 0:
                temperature_kelvin = data["main"]["temp"]
                temperature_celsius = temperature_kelvin - 273.15
                weather_description = data["weather"][0]["description"]
                return f"The temperature in {city} is {weather_description} with a temperature of {temperature_celsius:.1f}°C."
            else:
                today = datetime.datetime.now(datetime.timezone.utc).date()
                target_date = today + datetime.timedelta(days=day_offset)
                weather_list =  data["list"]
                target_forecasts = [
                    entry for entry in weather_list
                    if datetime.datetime.fromtimestamp(entry["dt"], tz=datetime.timezone.utc).date()==target_date
                ]
                if not target_forecasts:
                    return f"Sorry,i couldn't find the weather for {city} on {target_date}."
                avg_temp = sum(entry["main"]["temp"] for entry in target_forecasts)/len(target_forecasts)
                avg_temp_celsius = avg_temp - 273.15
                weather_description = [entry["weather"][0]["description"] for entry in target_forecasts]
                most_common_weather = max(set(weather_description), key=weather_description.count)
                return f"The weather in {city} on {target_date} is expected to be '{most_common_weather}'"
        else:
            return "Are you sure you living in earth?"
    except  Exception as e:
        return "An error occurred while fetching weather data."

def generate_response(user_input):
    global context_memory
    try:
        time_response = get_time_info(user_input)
        if time_response:
            return time_response

        if re.search(r"how about(.+)", user_input.lower()):
            new_query = re.search(r"how about(.+)", user_input.lower()).group(1).strip()
            if context_memory["last_translation"]:
                return translate_text(new_query,context_memory["last_translation_lang"])
            if context_memory["last_defination"]:
                return get_definition(new_query)
            return "Could you clarify what you mean by 'how about'?"
        
        if "translate" in user_input.lower() and "to" in user_input.lower():
            match = re.search(r"translate (.+?) to (\w+)", user_input.lower())
            if match:
                text, lang = match.groups()
                context_memory["last_translation"] = text.strip()
                context_memory["last_translation_lang"] = lang.strip()
                save_context()
                return translate_text(text.strip(), lang.strip())
            
        define_match = re.search(r"define\s+(\w+)",user_input.lower())
        if define_match:
            word = define_match.group(1)
            context_memory["last_defination"] = word
            save_context()
            return get_definition(word)
        
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
            day_offset = 0
            if  "tomorrow" in user_input.lower():
                day_offset = 1
            elif "day after tomorrow" in user_input.lower():
                day_offset = 2
            if cities:
                city = cities[0]
                weather_info = get_weather(city, day_offset)
                return weather_info
            else:
                return "Please provide a city name."
        
        joke_keywords = ["joke", "funny", "tell me a joke"]
        if any(keyword in user_input.lower() for keyword in joke_keywords):
            context_memory["last_joke_requested"] = True
            save_context()
            return get_joke()
        if context_memory["last_joke_requested"] and "next" in user_input.lower():
            return get_joke()
        context_memory["last_joke_requested"] = False
        save_context()  # 存檔
        if "my name is" in user_input.lower():
            name_match = re.search(r"my name is (\w+)", user_input.lower())
            if name_match:
                context_memory["user_name"] = name_match.group(1)
                save_context()
                return f"Nice to meet you, {context_memory['user_name']}!"
        if "what is my name" in user_input.lower():
            if context_memory["user_name"]:
                return f"Your name is {context_memory['user_name']}!"
            else:
                return "I don't know your name yet.What's your name?"
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
