import spacy
import json
import re
from spellchecker import SpellChecker
from translation import translate_text
from weather import get_weather
from news import get_news
from joke import get_joke
from definition import get_definition
from quotes import get_quote
from utils import correct_spelling
from utils import preprocess_text
from times import get_time_info
from calculation import calculate_expression
from fact import get_random_fact
from horoscope import get_horoscope

nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()

context_memory = {
    "last_joke_requested" : False,
    "last_translation" : None,
    "last_definition" : None,
    "last_translation_lang" : None,
    "user_name" : None,
    "last_quote_requested" : False
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

def generate_response(user_input):
    global context_memory
    try:
        user_input = correct_spelling(user_input)
        time_response = get_time_info(user_input)
        if time_response:
            return time_response

        if "news" in user_input.lower() or "headlines" in user_input.lower():
            return get_news()
        
        if "quote" in user_input.lower():
            context_memory["last_quote_requested"] = True
            save_context()
            return get_quote()
        if context_memory["last_quote_requested"] and "next" in user_input.lower():
            return get_quote()
        context_memory["last_quote_requested"]=False
        save_context()
        
        if "random fact" in user_input.lower() or "fact" in user_input.lower():
            return get_random_fact()
        
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
                context_memory["last_defination"] = None
                save_context()
                return translate_text(text.strip(), lang.strip())
            
        define_match = re.search(r"define\s+(\w+)",user_input.lower())
        if define_match:
            word = define_match.group(1)
            context_memory["last_defination"] = word
            context_memory["last_translation"] = None
            save_context()
            return get_definition(word)

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

        if "horoscope" in user_input.lower():
             user_input = user_input.strip().lower()  # 清理輸入
        print(f"Debug: User input = {user_input}")  # 打印用戶輸入

        # 使用正則表達式匹配星座名稱
        match = re.search(r"horoscope\s+for\s+(\w+)", user_input)
        if match:
            sign = match.group(1).strip().lower()
            print(f"Debug: Matched sign = {sign}")  # 打印匹配到的星座

            # 檢查星座名稱是否有效
            valid_signs = {"aries", "taurus", "gemini", "cancer", "leo", "virgo", 
                           "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"}
            if sign in valid_signs:
                return get_horoscope(sign)
            else:
                return "Please provide a valid zodiac sign."
        else:
            print("Debug: No match found")  # 打印未匹配到的信息
        
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
            return"I like to chat with you!"
        return "I'm not sure how to respond to that."
    
    except Exception as e:
        import traceback
        print(f"Error in generate_response: {e}")
        traceback.print_exc()
        return "Sorry, an error occurred while processing your request."
