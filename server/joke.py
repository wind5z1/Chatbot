import requests

# ランダムなジョークを取得する関数
def get_joke():
    try:
        # ジョークAPIのURL
        url = "https://api.chucknorris.io/jokes/random"
        
        # GETリクエストを送信
        response = requests.get(url)
        
        # ステータスコードが200（成功）の場合
        if response.status_code == 200:
            # JSONデータを取得し、ジョークの部分を返す
            data = response.json()
            return data["value"]
        else:
            # APIリクエストが失敗した場合のメッセージ
            return "今はジョークが思いつかないよ…ちょっと考えさせて！"
    except Exception as e:
        # エラーが発生した場合のメッセージ
        return "ジョークを取得する際にエラーが発生しました。"
