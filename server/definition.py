import requests

# 単語の定義を取得する関数
def get_definition(word):
    # 辞書APIのURL（指定した単語の定義を取得）
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    
    # GETリクエストを送信
    response = requests.get(url)

    # ステータスコードが200（成功）の場合
    if response.status_code == 200:
        try:
            # JSONデータを取得し、定義を抽出
            data = response.json()
            # 正しいJSON解析パス
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            return f"'{word}' の定義: {definition}"
        except (KeyError, IndexError) as e:
            # JSON構造が一致しない、または必要なフィールドが欠けている場合
            return f"I'm sorry、The define of '{word}' is not found."
    else:
        # APIリクエストが失敗した場合
        return f"I'm sorry、The define of word '{word}' is not found."
