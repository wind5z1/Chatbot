import subprocess
import contractions
import spacy
import platform

# 下載 NLTK 必需的資料
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    text = contractions.fix(text)
    doc = nlp(text.lower())

    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
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

def generate_response(user_input):
    try:
        app_command = check_for_app_command(user_input)
        if app_command:
            open_app(app_command)
            return f"Opening {app_command}..."
        
        tokens = preprocess_text(user_input)
        user_sentences = " ".join(tokens)

        greetings = ["hello", "hi", "hey"]
        farewells = ["goodbye", "bye", "see you later"]
        help_intents = ["help", "what can you do"]
        favorites = ["favourite", "love", "like"]

        if any(greeting in user_sentences for greeting in greetings):
            return "Hello! How can I assist you today?"
        elif any(farewell in user_sentences for farewell in farewells):
            return "Goodbye! Have a nice day!"
        elif any(help_intent in user_sentences for help_intent in help_intents):
            return "I can chat with you in simple conversations. You can ask me anything!"
        elif any(favourite in user_sentences for favourite in favorites):
            return "I like to chat with you!"
        return "I'm not sure how to respond to that."
    
    except Exception as e:
        import traceback
        print(f"Error in generate_response: {e}")
        traceback.print_exc()
        return "Sorry, an error occurred while processing your request."
