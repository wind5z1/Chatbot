import spacy
import pytz
import datetime
nlp = spacy.load("en_core_web_sm")
def get_time_info(user_input):
    doc = nlp(user_input.lower())

    # 檢查是否提到 "time" 或 "date"
    if "time" in user_input.lower() or "date" in user_input.lower():
        # 嘗試從句子中找出地點（GPE = 地理位置實體）
        locations = [ent.text.lower() for ent in doc.ents if ent.label_ == "GPE"]

        # 城市對應的時區
        timezone_map = {
            "new york": "America/New_York",
            "london": "Europe/London",
            "paris": "Europe/Paris",
            "tokyo": "Asia/Tokyo",
            "beijing": "Asia/Shanghai",
            "hong kong": "Asia/Hong_Kong",
            "taipei": "Asia/Taipei",
            "sydney": "Australia/Sydney",
            "los angeles": "America/Los_Angeles",
            "malaysia": "Asia/Kuala_Lumpur",
            "singapore": "Asia/Singapore",
            "korea": "Asia/Seoul"
        }

        # 國家對應的主要城市
        country_timezone_map = {
            "japan": "tokyo",
            "china": "beijing",
            "usa": "new york",
            "america": "new york",
            "australia": "sydney",
            "uk": "london",
            "united kingdom": "london",
            "france": "paris",
            "taiwan": "taipei",
            "singapore": "singapore",
            "malaysia": "malaysia",
            "korea": "korea"
        }

        if locations:
            location = locations[0]

            # 如果輸入的是國家名稱，轉換為城市名稱
            if location in country_timezone_map:
                location = country_timezone_map[location]

            # 檢查城市是否在時區對應表內
            if location in timezone_map:
                tz = pytz.timezone(timezone_map[location])
                now = datetime.datetime.now(tz)
                if "time" in user_input.lower():
                    return f"The current time in {location.title()} is {now.strftime('%H:%M:%S')}."
                elif "date" in user_input.lower():
                    return f"The current date in {location.title()} is {now.strftime('%Y-%m-%d')}."
            else:
                return "Sorry, I don't know the timezone for that location. Please try another city."
        
        # 如果沒有提供地點，就返回 UTC 時間
        now = datetime.datetime.utcnow()
        if "time" in user_input.lower():
            return f"The current UTC time is {now.strftime('%H:%M:%S')}."
        elif "date" in user_input.lower():
            return f"The current UTC date is {now.strftime('%Y-%m-%d')}."
    
    return None  # 如果沒有符合的條件，返回 None