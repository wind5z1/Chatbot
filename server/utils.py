import contractions
import spacy
from spellchecker import SpellChecker

nlp = spacy.load("en_core_web_sm")
spell = SpellChecker()

def correct_spelling(text):
    words = text.split()
    corrected_words = []
    for word in words:
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word)
    return ' '.join(corrected_words)

def preprocess_text(text):
    text = contractions.fix(text)
    doc = nlp(text.lower())

    tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]
    return tokens
