import subprocess
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# 下載 NLTK 必需的資料
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def check_for_app_command(user_input):
    tokens = word_tokenize(user_input.lower())
    pos_tags = pos_tag(tokens)
    for token, tag in pos_tags:
        if tag == 'NN' and token in ['calculator', 'notepad', 'chrome']:  # ✅ 修正條件判斷
            return token
    return None

def open_app(app_name):
    if app_name == 'calculator':
        subprocess.Popen(['calc.exe'])
    elif app_name == 'notepad':
        subprocess.Popen(['notepad.exe'])
    elif app_name == 'chrome':
        subprocess.Popen(['chrome.exe'])

def generate_response(user_input):
    tokens = word_tokenize(user_input.lower())
    greetings = ["hello", "hi", "hey", "how are you", "what's up"]
    farewells = ["goodbye", "bye", "see you later"]
    help_intents = ["help", "what can you do", "what can you help with"]
    favorites = ["favourite", "love", "like"]

    if any(token in greetings for token in tokens):
        return "Hello! How can I assist you today?"
    elif any(token in farewells for token in tokens):
        return "Goodbye! Have a nice day!"
    elif any(token in help_intents for token in tokens):
        return "I can chat with you in simple conversations. You can ask me anything!"
    elif any(token in favorites for token in tokens):
        return "I like to chat with you!"
    else:
        return "I'm sorry, I don't understand. Can you please rephrase your question?"



