import requests

def get_horoscope(sign):
    api_key="wdfR4kswJ07sTVhmDtrHS5MckXZQYHzg4eUA0Xeu"
    url=f"https://json.freeastrologyapi.com/western/houses/{sign}/daily?apikey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        horoscope_data = response.json()
        return horoscope_data.get("horoscope","No horoscope information found.")
    else:
        return "I didn't have any horoscope imformation at this moment.Let me think a bit..."