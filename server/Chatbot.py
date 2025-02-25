import subprocess
import contractions
import spacy
import platform
import requests
import re
import math
import operator as op

# 下載 NLTK 必需的資料
nlp = spacy.load("en_core_web_sm")

operators ={
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
        expression = expression.replace(" ", " ")
        expression = re.sub(r'(\d+)%', lambda m: str(float(m.group(1)) + "/100"), expression)
        if not re.match(r'^[\d+\-*/().% a-zA-Z]+$', expression): 
            return "Invalid expression,Please try again."
        result = eval(expression, {"__builtins__": None}, {**operators, **math_functions})
        return f"The result is: {result}"
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except Exception as e:
        return f"Error calculating expression: {str(e)}"
    
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
    try:
        app_command = check_for_app_command(user_input)
        if app_command:
            open_app(app_command)
            return f"Opening {app_command}..."
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
        
        if any(char in user_input for char in "0123456789+-*/^%") or \
            any(func in user_input.lower() for func in ["sqrt", "sin", "cos", "tan", "log"]):
            expression = re.sub(r'[^0-9+\-*/().% ]', '', user_input)
            if expression:
                return calculate_expression(expression)
            else:
                return "Please provide a valid mathematical expression."
        
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
