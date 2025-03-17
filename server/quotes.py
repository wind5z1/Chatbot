import requests
def get_quote():
    url="https://zenquotes.io/api/random"
    try:
        response = requests.get(url)
        if response.status_code==200:
            data=response.json()
            quote = data[0].get("q", "No quote found.")
            author = data[0].get("a", "Unknown")
            return f"Here's a quote for you:\n\n\"{quote}\"\n- {author}"
        else:
            return f"Let me think what quote can i choose for you..."
    except Exception as e:
        return f"An error occured while fetching the quote: str(e)"

    