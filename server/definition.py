import requests

def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            # 正確的 JSON 解析路徑
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            return f"Definition of '{word}': {definition}"
        except (KeyError, IndexError) as e:
            # 如果 JSON 結構不匹配或缺少字段
            return f"Sorry, I couldn't find the definition of the word '{word}'."
    else:
        # 如果 API 請求失敗
        return f"Sorry, I couldn't find the definition of the word '{word}'."
