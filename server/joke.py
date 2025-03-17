import requests

def get_joke():
    try:
        url = "https://api.chucknorris.io/jokes/random"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["value"]
        else:
            return "I didn't have any jokes at this moment.Let me think a bit..."
    except Exception as e:
        return "An error occurred while fetching a joke."