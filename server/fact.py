import requests

def get_random_fact():
    url="https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)

    if response.status_code == 200:
        fact_data = response.json()
        return fact_data["text"]
    else:
        return "I didn't have any fun facts at this moment.Let me think a bit..."