import requests

def get_horoscope(sign):
    url=f"https://json.freeastrologyapi.com/horoscope/{sign}/daily"
    headers = {
        "Authorization": "Bearer wdfR4kswJ07sTVhmDtrHS5MckXZQYHzg4eUA0Xeu"
    }
    response = requests.get(url, headers=headers)

    print(f"Status Code: {response.status_code}")  # 打印 HTTP 状态码
    print(f"Response Text: {response.text}")  # 打印 API 返回的文本内容

    if response.status_code == 200:
        horoscope_data = response.json()
        return horoscope_data.get("horoscope","No horoscope information found.")
    else:
        return "I didn't have any horoscope imformation at this moment.Let me think a bit..."