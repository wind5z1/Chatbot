from deep_translator import GoogleTranslator
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