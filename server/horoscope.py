import requests

def get_horoscope(sign):
    url = "https://best-daily-astrology-and-horoscope-api.p.rapidapi.com/api/Detailed-Horoscope/"
    querystring = {"zodiacSign": sign}

    headers = {
        "X-RapidAPI-Key": "0bde6d52ccmsh7e12e7c52ee3d68p119f1djsn84b655af5bb6",  # 替換為你的 RapidAPI 密鑰
        "X-RapidAPI-Host": "best-daily-astrology-and-horoscope-api.p.rapidapi.com"
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.json()
        else:
            return "I didn't have any horoscope at this moment.Let me think a bit..."
    except requests.exceptions.RequestException as e:
        return f"An Error occured: {e}"