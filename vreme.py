import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.express as px

# Конфигурация
API_KEY = "4a52e4f76c6dd2875d8afec3fc6ec215"
CITY = "Plovdiv"
URL = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

# Нормални стойности за месеци
NORMALS = {
    "April": {"temp": 14, "rain_days": 7},
    "May": {"temp": 18, "rain_days": 9}
}

# Функция за извличане на прогнозни метео данни
def get_weather_data():
    response = requests.get(URL)
    data = response.json()
    weather = []

    for entry in data["list"]:
        date = datetime.fromtimestamp(entry["dt"]).date()
        temp = entry["main"]["temp"]
        rain = entry.get("rain", {}).get("3h", 0)
        humidity = entry["main"]["humidity"]
        weather.append({
            "date": date,
            "temp": temp,
            "rain": rain,
            "humidity": humidity
        })

    df = pd.DataFrame(weather)
    df = df.groupby("date").agg({
        "temp": "mean",
        "rain": "sum",
        "humidity": "mean"
    })
    return df

# Основно приложение
st.title("Метео анализ за Пловдив 🌍")
st.write("Анализ на температурите и валежите спрямо нормите за месеца.")

# Извличане на данни
st.header("1. Данни за времето")
st.write("Извличане на данни от OpenWeatherMap за Пловдив.")
weather_df = get_weather_data()
st.dataframe(weather_df)

# Визуализация
st.header("2. Визуализация на данните")
fig_temp = px.line(weather_df, x=weather_df.index, y="temp", title="Температура по дни (°C)")
fig_rain = px.bar(weather_df, x=weather_df.index, y="rain", title="Валежи по дни (mm)")
st.plotly_chart(fig_temp)
st.plotly_chart(fig_rain)

# Сравнение с нормите
st.header("3. Анализ на времето спрямо нормите")
current_month = datetime.now().strftime("%B")
avg_temp = weather_df["temp"].mean()
rain_days = (weather_df["rain"] > 0).sum()

st.write(f"Средна температура за {current_month}: {avg_temp:.1f}°C")
st.write(f"Дни с валежи: {rain_days}")

if avg_temp > NORMALS[current_month]["temp"] + 2:
    st.warning("⚠️ Температурите са необичайно високи!")
else:
    st.success("✅ Температурите са в норма.")

if rain_days > NORMALS[current_month]["rain_days"]:
    st.warning("⚠️ Има повече дъждовни дни от обичайното!")
else:
    st.success("✅ Валежите са в норма.")
