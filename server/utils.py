import contractions
import spacy
from spellchecker import SpellChecker

# spaCy を使用して英語のテキストを処理する
nlp = spacy.load("en_core_web_sm")
# スペルチェッカーの初期化
spell = SpellChecker()

# テキストのスペルを修正する関数
def correct_spelling(text):
    # テキストを単語に分割
    words = text.split()
    corrected_words = []
    
    # 各単語のスペルを修正
    for word in words:
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word)
    
    # 修正された単語を再び結合して返す
    return ' '.join(corrected_words)

# テキストを前処理する関数
def preprocess_text(text):
    # テキストの縮約形（例: don't -> do not）を展開
    text = contractions.fix(text)
    
    # テキストを小文字に変換し、spaCy で処理
    doc = nlp(text.lower())
    
    # ストップワードを除き、アルファベットの単語だけをリストに格納
    tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]
    
    # トークン（単語）のリストを返す
    return tokens
