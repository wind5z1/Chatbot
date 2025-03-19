import requests

def get_horoscope(sign):
    url = f"https://best-daily-astrology-and-horoscope-api.p.rapidapi.com/api/Detailed-Horoscope/?zodiacSign={sign}"
    headers = {
        "X-RapidAPI-Key": "0bde6d52ccmsh7e12e7c52ee3d68p119f1djsn84b655af5bb6",  # 替換為你的 RapidAPI 密鑰
        "X-RapidAPI-Host": "best-daily-astrology-and-horoscope-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return "Failed to fetch horoscope."