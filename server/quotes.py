import requests

# ランダムな名言を取得する関数
def get_quote():
    # ZenQuotes API のURL（ランダムな名言を取得）
    url = "https://zenquotes.io/api/random"
    
    try:
        # GET リクエストを送信
        response = requests.get(url)
        
        # ステータスコードが 200（成功）の場合
        if response.status_code == 200:
            # JSON データを取得
            data = response.json()
            
            # 名言と著者を抽出（デフォルト値を設定）
            quote = data[0].get("q", "Cannot find quote")
            author = data[0].get("a", "Unknown author")
            
            # 名言をフォーマットして返す
            return f"Your quote is:\n\n\"{quote}\"\n- {author}"
        else:
            # API リクエストが失敗した場合のメッセージ
            return f"I'm thinking which quote matches you..."
    except Exception as e:
        # エラーが発生した場合のメッセージ
        return f"There is a problem while fetching a quote: {str(e)}"
