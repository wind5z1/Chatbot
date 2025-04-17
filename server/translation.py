from deep_translator import GoogleTranslator

# テキストを指定された言語に翻訳する関数
def translate_text(text, target_language):
    try:
        # テキストが空白の場合、翻訳できない旨を返す
        if not text.strip():
            return "翻訳するテキストを提供してください。"
        
        # 対象言語に対応する言語コードのマップ
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
        
        # 対象言語がマップに存在する場合はそのコードを使用
        target_language = language_map.get(target_language.lower(), target_language)
        
        # GoogleTranslator を使って翻訳を実行
        translated = GoogleTranslator(source='auto', target=target_language).translate(text)
        
        # 翻訳結果が存在する場合、翻訳されたテキストを返す
        if translated:
            return f"{translated}"
        else:
            # 翻訳に失敗した場合のメッセージ
            return "翻訳に失敗しました。もう一度試してください。"
    except Exception as e:
        # エラーが発生した場合のエラーメッセージ
        return f"翻訳中にエラーが発生しました: {str(e)}"
