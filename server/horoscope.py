import requests

def get_horoscope():
    url = "https://json.freeastrologyapi.com/western/planets"

# API 密鑰（這裡需要你自己的密鑰）
    api_key = "wdfR4kswJ07sTVhmDtrHS5MckXZQYHzg4eUA0Xeu"

# 添加 API 密鑰到請求頭部（如果 API 需要這樣）
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

# 發送 GET 請求
    response = requests.get(url, headers=headers)

# 檢查響應狀態
    if response.status_code == 200:
        # 解析並顯示返回的 JSON 數據
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code}, {response.text}")