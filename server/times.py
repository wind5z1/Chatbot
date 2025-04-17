import spacy
import pytz
import datetime

# spaCy を使用して英語のテキストを処理する
nlp = spacy.load("en_core_web_sm")

# ユーザーの入力から時間情報を取得する関数
def get_time_info(user_input):
    doc = nlp(user_input.lower())

    # "time" または "date" が含まれているか確認
    if "time" in user_input.lower() or "date" in user_input.lower():
        # 文章から場所（GPE = 地理的な位置）を取得
        locations = [ent.text.lower() for ent in doc.ents if ent.label_ == "GPE"]

        # 都市ごとのタイムゾーンマップ
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

        # 国名に対応する主要都市
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

            # 入力された場所が国名の場合、それに対応する都市名に変換
            if location in country_timezone_map:
                location = country_timezone_map[location]

            # 都市名がタイムゾーンマップに含まれているか確認
            if location in timezone_map:
                tz = pytz.timezone(timezone_map[location])
                now = datetime.datetime.now(tz)
                
                # "time" が含まれていれば、現在の時刻を返す
                if "time" in user_input.lower():
                    return f"The time in {location.title()} now is {now.strftime('%H:%M:%S')}"
                # "date" が含まれていれば、現在の日付を返す
                elif "date" in user_input.lower():
                    return f"The date in{location.title()} today is {now.strftime('%Y-%m-%d')}"
            else:
                # タイムゾーン情報が見つからない場合
                return "The timezone information could not be found.Please try other locations."
        
        # 場所が提供されていない場合、UTC 時間を返す
        now = datetime.datetime.utcnow()
        if "time" in user_input.lower():
            return f"The current UTC time is {now.strftime('%H:%M:%S')}"
        elif "date" in user_input.lower():
            return f"The current UTC date is {now.strftime('%Y-%m-%d')}"
    
    return None  # 条件に一致しない場合は None を返す
