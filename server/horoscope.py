import requests

def get_horoscope(zodiac_sign, day="today"):
    url=f"https://aztro.sameerkumar.website?sign={zodiac_sign}&day={day}"
    response = requests.post(url)
    if response.status_code == 200:
        horoscope_data = response.json()
        return horoscope_data["description"]
    else:
        return "I didn't have any horoscope imformation at this moment.Let me think a bit..."