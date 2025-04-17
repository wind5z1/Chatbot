import requests
# 占星情報を取得する関数（星座を引数として受け取る）
def get_horoscope(sign):
    url = "https://json.freeastrologyapi.com/western/planets"

    # APIキー
    api_key = "wdfR4kswJ07sTVhmDtrHS5MckXZQYHzg4eUA0Xeu"

    # リクエストヘッダーにAPIキーを追加
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # GETリクエストを送信
    response = requests.get(url, headers=headers)

    # レスポンスのステータスを確認
    if response.status_code == 200:
        # JSONデータを解析して表示
        data = response.json()
        print(data)
    else:
        print(f"エラー: {response.status_code}, {response.text}")
