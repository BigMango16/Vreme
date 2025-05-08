import requests

def get_weather(zip_code, country_code, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?zip={4000},{359}&appid={4a52e4f76c6dd2875d8afec3fc6ec215}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        city = data['name']
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        
        print(f"Времето в {city}:")
        print(f"Температура: {temperature}°C")
        print(f"Описание: {weather_description.capitalize()}")
        print(f"Влажност: {humidity}%")
        print(f"Скорост на вятъра: {wind_speed} м/с")
    else:
        print(f"Неуспешно извличане на данни за времето. Код на грешка: {response.status_code}")

if __name__ == "__main__":
    # Въведете вашия zip код и код на държавата
    zip_code = input("Въведете ZIP код: ")
    country_code = input("Въведете код на държавата (например BG за България): ")
    
    # API ключ
    api_key = "4a52e4f76c6dd2875d8afec3fc6ec215"
    
    # Извличане на информация за времето
    get_weather(zip_code, country_code, api_key)
