import subprocess
import contractions
import spacy
import platform
import requests
import re
import math
import operator as op
from deep_translator import GoogleTranslator

# 下載 NLTK 必需的資料
nlp = spacy.load("en_core_web_sm")

last_joke_requested = False
last_translation_text = None
last_translation_lang = None
last_definition_word = None

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
    global last_joke_requested, last_definition_word, last_translation_text, last_translation_lang
    try:
        if "next" in user_input.lower():
            if last_translation_lang and last_translation_text:
                return translate_text(last_translation_text,last_translation_lang)
            elif last_definition_word:
                return get_definition(last_definition_word)
            else:
                return "What you mean about {user_input}?"
        define_match = re.search(r"define\s+(\w+)", user_input.lower())
        if define_match:
            word = define_match.group(1)
            last_definition_word = word
            return get_definition(word)

        if "translate" in user_input.lower() and "to" in user_input.lower():
            match = re.search(r"translate (.+?) to (\w+)", user_input.lower())
            if match:
                text, lang = match.groups()
                if text.strip() and lang.strip():
                    last_translation_lang = text.strip()
                    last_translation_text = lang.strip()
                    return translate_text(text.strip(), lang.strip())
                else:
                    "Please provide both text and target language."
            else:
                return "Please use the format: translate [your text] to [desired language]."

        if last_translation_lang:
            if re.match(r"^[a-zA-Z\s]+$", user_input.strip()):
                last_translation_text = user_input.strip()
                return translate_text(user_input.strip(), last_translation_lang)
            else:
                return "Please provide a valid text."
            
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
