import requests

def get_horoscope(sign):
    url=f"https://aztro.sameerkumar.website/?sign={sign}&day=today"
    response = requests.post(url)
    if response.status_code == 200:
        horoscope_data = response.json()
        return  f"Horoscope for {sign.capitalize()}: {horoscope_data['description']}"
    else:
        return "I didn't have any horoscope imformation at this moment.Let me think a bit..."