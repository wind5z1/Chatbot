import requests

def get_horoscope(zodiac_sign):
    url=f"https://horoscope-api.herokuapp.com/horoscope/today/{zodiac_sign}"
    response = requests.get(url)
    if response.status_code == 200:
        horoscope_data = response.json()
        return horoscope_data["horoscope"]
    else:
        return "I didn't have any horoscope imformation at this moment.Let me think a bit..."