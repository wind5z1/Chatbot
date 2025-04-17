import requests
import datetime

# 天気情報を取得する関数
def get_weather(city, day_offset):
    # OpenWeatherMap の API キー
    api_key = "5dac3b051c407fc1fcc3b4d8e6043446"
    
    # 今日の天気情報を取得する場合
    if day_offset == 0:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    # 未来の天気予報を取得する場合
    else:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

    try:
        # API にリクエストを送信
        response = requests.get(url)
        
        # ステータスコードが 200 (成功) の場合
        if response.status_code == 200:
            data = response.json()
            
            # 今日の天気情報を取得する場合
            if day_offset == 0:
                # ケルビン温度を摂氏に変換
                temperature_kelvin = data["main"]["temp"]
                temperature_celsius = temperature_kelvin - 273.15
                weather_description = data["weather"][0]["description"]
                
                return f"{city} today's weather is {weather_description} and the temperature is {temperature_celsius:.1f}"
            else:
                # 今日の日付を取得
                today = datetime.datetime.now(datetime.timezone.utc).date()
                target_date = today + datetime.timedelta(days=day_offset)
                
                # 未来の天気予報を取得
                weather_list = data["list"]
                target_forecasts = [
                    entry for entry in weather_list
                    if datetime.datetime.fromtimestamp(entry["dt"], tz=datetime.timezone.utc).date() == target_date
                ]
                
                # 指定された日付に天気予報が見つからない場合
                if not target_forecasts:
                    return f"I'm sorry, i couldn't find weather forecast for {city} on {target_date} "
                
                # 指定日付の予報の平均温度を計算
                avg_temp = sum(entry["main"]["temp"] for entry in target_forecasts) / len(target_forecasts)
                avg_temp_celsius = avg_temp - 273.15
                
                # 天気の説明の最も一般的なものを取得
                weather_description = [entry["weather"][0]["description"] for entry in target_forecasts]
                most_common_weather = max(set(weather_description), key=weather_description.count)
                
                return f"Weather of{city} on {target_date} is preficted as '{most_common_weather}'."
        else:
            # API のリクエストが失敗した場合
            return "You sure you live in Earth?"
    except Exception as e:
        # 何らかのエラーが発生した場合
        return "An error occurred while fetching weather information. Please try again later."
