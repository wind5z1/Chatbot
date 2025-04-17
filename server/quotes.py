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
            quote = data[0].get("q", "名言が見つかりませんでした。")
            author = data[0].get("a", "不明")
            
            # 名言をフォーマットして返す
            return f"あなたへの名言です:\n\n\"{quote}\"\n- {author}"
        else:
            # API リクエストが失敗した場合のメッセージ
            return f"どの名言を選ぶか考え中です…"
    except Exception as e:
        # エラーが発生した場合のメッセージ
        return f"名言を取得する際にエラーが発生しました: {str(e)}"
