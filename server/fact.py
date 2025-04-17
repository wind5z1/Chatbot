import requests

# ランダムな雑学（ファンファクト）を取得する関数
def get_random_fact():
    # API のURL（英語の無駄知識を取得）
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    
    # GETリクエストを送信
    response = requests.get(url)

    # ステータスコードが200（成功）の場合
    if response.status_code == 200:
        # JSONデータを取得して、テキスト部分を返す
        fact_data = response.json()
        return fact_data["text"]
    else:
        # エラー時のメッセージを返す
        return "今は面白い雑学が思いつかないよ…ちょっと考えさせて！"
