import requests
import datetime
def get_weather(city, day_offset):
    api_key = "5dac3b051c407fc1fcc3b4d8e6043446"
    if day_offset == 0:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    else:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if day_offset == 0:
                temperature_kelvin = data["main"]["temp"]
                temperature_celsius = temperature_kelvin - 273.15
                weather_description = data["weather"][0]["description"]
                return f"The temperature in {city} is {weather_description} with a temperature of {temperature_celsius:.1f}°C."
            else:
                today = datetime.datetime.now(datetime.timezone.utc).date()
                target_date = today + datetime.timedelta(days=day_offset)
                weather_list =  data["list"]
                target_forecasts = [
                    entry for entry in weather_list
                    if datetime.datetime.fromtimestamp(entry["dt"], tz=datetime.timezone.utc).date()==target_date
                ]
                if not target_forecasts:
                    return f"Sorry,i couldn't find the weather for {city} on {target_date}."
                avg_temp = sum(entry["main"]["temp"] for entry in target_forecasts)/len(target_forecasts)
                avg_temp_celsius = avg_temp - 273.15
                weather_description = [entry["weather"][0]["description"] for entry in target_forecasts]
                most_common_weather = max(set(weather_description), key=weather_description.count)
                return f"The weather in {city} on {target_date} is expected to be '{most_common_weather}'"
        else:
            return "Are you sure you living in earth?"
    except  Exception as e:
        return "An error occurred while fetching weather data."