import requests

def get_horoscope(sign):
    url=f"https://json.freeastrologyapi.com/horoscope/{sign}/daily"
    headers = {
        "Authorization": "Bearer wdfR4kswJ07sTVhmDtrHS5MckXZQYHzg4eUA0Xeu"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        horoscope_data = response.json()
        return horoscope_data.get("horoscope","No horoscope information found.")
    else:
        return "I didn't have any horoscope imformation at this moment.Let me think a bit..."