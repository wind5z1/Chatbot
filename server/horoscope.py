import requests

def get_horoscope(sign):
    url = "https://json.freeastrologyapi.com/horoscope/daily"  # 請確保這是正確的端點
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "wdfR4kswJ07sTVhmDtrHS5MckXZQYHzg4eUA0Xeu"  # 替換為你的 API 密鑰
    }
    # 在 POST 請求中發送星座信息（例如："aries", "leo"）
    data = {
        "sign": sign  # 這裡 "sign" 是你想查詢的星座
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()  # 返回 JSON 格式的運勢資料
    else:
        return f"Failed to fetch horoscope. Status code: {response.status_code}"