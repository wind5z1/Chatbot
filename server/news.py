import requests

# 最新のニュースヘッドラインを取得する関数
def get_news():
    # NewsAPI の API キー（ここでは US のニュースを取得）
    api_key = "1087b5b718d54d5293369d275c13d2d8"
    
    # NewsAPI の URL（US のトップニュースを取得）
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    
    try:
        # GET リクエストを送信
        response = requests.get(url)
        
        # ステータスコードが 200（成功）の場合
        if response.status_code == 200:
            # JSON データを取得
            data = response.json()
            
            # 記事リストを取得
            articles = response.json().get("articles", [])
            
            # 記事タイトルと説明をリストにまとめる
            news_list = [f"{article['title']}:{article['description']}" for article in articles]
            
            # ニュースのヘッドラインを返す
            return "Here is the latest news:\n" + "\n".join(news_list)
        else:
            # API リクエストが失敗した場合
            return "I can't find any news right now. Let me think about it..."
    except Exception as e:
        # エラーが発生した場合
        return f"An error occurred while fetching news: {str(e)}"
