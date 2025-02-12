import subprocess
import nltk
import sys
from nltk.tokenize import word_tokenize
from nltk import pos_tag

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')

def check_for_app_command(user_input):
    tokens = word_tokenize(user_input.lower())
    pos_tags = pos_tag(tokens)
    for token, tag in pos_tags:
        if tag == 'NN' and token == ['calculator', 'notepad', 'chrome']:
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
        print("Bot: Goodbye! Have a nice day!")
        sys.exit()
    elif any(token in help_intents for token in tokens):
        return "I can chat with you in simple convertations. You can ask me anything!"
    elif any(token in favorites for token in tokens):
        return "I like to chat with you!"
    else:
        return "I'm sorry, I don't understand. Can you please rephrase your question?"
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break
    response = generate_response(user_input)
    print("Bot:", response)
    app_name = check_for_app_command(user_input)
    if app_name:
        open_app(app_name)
    else:
        print("Bot: I'm sorry, I don't know how to open that app.")