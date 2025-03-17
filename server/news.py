import requests
def get_news():
    api_key="1087b5b718d54d5293369d275c13d2d8"
    url=f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles=response.json().get("articles", [])
            news_list=[f"{article['title']}:{article['description']}"for article in articles]
            return "Here are the latest news headlines in us:\n" + "\n".join(news_list)
        else:
            return "I didn't have any news at this moment.Let me think a bit..."
    except Exception as e:
        return f"An error occurred while fetching news."