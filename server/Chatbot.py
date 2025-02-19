import subprocess
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# 下載 NLTK 必需的資料
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

def check_for_app_command(user_input):
    tokens = word_tokenize(user_input.lower())
    pos_tags = pos_tag(tokens)
    for token, tag in pos_tags:
        if tag == 'NN' and token in ['calculator', 'notepad']:  # ✅ 修正條件判斷
            return token
    return None

def open_app(app_name):
    if app_name == 'calculator':
        subprocess.run(['calc'], shell=True)
    elif app_name == 'notepad':
        subprocess.run(['notepad'], shell=True)
    else:
        print(f"Unknown app: {app_name}")

def generate_response(user_input):
    try:
        app_command = check_for_app_command(user_input)
        if app_command:
            open_app(app_command)
            return f"Opening {app_command}..."
        
        tokens = word_tokenize(user_input.lower())
        user_sentences = " ".join(tokens)
        greetings = ["hello", "hi", "hey", "how are you", "what's up"]
        farewells = ["goodbye", "bye", "see you later"]
        help_intents = ["help", "what can you do", "what can you help with"]
        favorites = ["favourite", "love", "like"]

        if any(token in greetings for token in tokens):
            return "Hello! How can I assist you today?"
        elif any(token in farewells for token in tokens):
            return "Goodbye! Have a nice day!"
        elif any(intent in user_sentences for intent in help_intents):
            return "I can chat with you in simple conversations. You can ask me anything!"
        elif any(token in favorites for token in tokens):
            return "I like to chat with you!"
        return "I'm not sure how to respond that."
    except Exception as e:
        print(f"Error in generate response: {e}")
        return "Sorry, I couldn't understand you. Can you please rephrase your question?"




