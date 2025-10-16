import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from gtts import gTTS
from playsound import playsound
import os
import datetime
import io
import pandas as pd
import matplotlib.pyplot as plt

# Global variable for TTS text
podcast_text = ""

# ================= WEATHER FETCH FUNCTION =================
def get_weather():
    global podcast_text
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name!")
        return

    api_key = "db1dff1168c65f0891ce034b3566cda8"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    url = f"{base_url}appid={api_key}&q={city}&units=metric"

    weather_label.config(text="Fetching weather details...", fg="white")
    icon_label.config(image='')

    try:
        response = requests.get(url)
        weather_data = response.json()

        if weather_data.get("cod") != 200:
            messagebox.showerror("Error", weather_data.get("message", "City not found"))
            return

        # Extract data
        temp = weather_data['main']['temp']
        temp_f = round(temp * 9/5 + 32, 2)
        feels = weather_data['main']['feels_like']
        pressure = weather_data['main']['pressure']
        humidity = weather_data['main']['humidity']
        desc = weather_data['weather'][0]['description'].capitalize()
        wind = weather_data['wind']['speed']
        visibility = weather_data.get('visibility', 0) / 1000
        clouds = weather_data['clouds']['all']

        sunrise = datetime.datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')
        current_time = datetime.datetime.now().strftime("%d %b %Y | %I:%M %p")

        # Format display text
        weather_text = (
            f"📍 City: {city}\n"
            f"🕓 Report Time: {current_time}\n\n"
            f"🌡 Temperature: {temp}°C | {temp_f}°F\n"
            f"😌 Feels Like: {feels}°C\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬 Wind Speed: {wind} m/s\n"
            f"☁ Clouds: {clouds}%\n"
            f"👀 Visibility: {visibility} km\n"
            f"🔼 Pressure: {pressure} hPa\n"
            f"🌅 Sunrise: {sunrise}\n"
            f"🌇 Sunset: {sunset}\n\n"
            f"📖 Description: {desc}"
        )

        weather_label.config(text=weather_text, fg="white")

        # Weather Icon
        icon_name = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_name}@4x.png"
        icon_data = requests.get(icon_url).content
        icon_image = Image.open(io.BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo

        # Store text for TTS
        podcast_text = f"The weather in {city} is {desc}. The temperature is {temp} degree Celsius. Humidity is {humidity} percent and wind speed is {wind} meters per second."

        # Save Data for Trend Analysis
        save_weather_data(city, temp, humidity, desc)

    except Exception as e:
        messagebox.showerror("Error", f"Unable to fetch weather data.\n{e}")

# ================= SAVE WEATHER DATA FUNCTION =================
def save_weather_data(city, temp, humidity, desc):
    data = {
        "Date": [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "City": [city],
        "Temperature": [temp],
        "Humidity": [humidity],
        "Condition": [desc]
    }

    df = pd.DataFrame(data)

    if os.path.exists("weather_log.csv"):
        df.to_csv("weather_log.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("weather_log.csv", index=False)

# ================= ANALYZE TREND FUNCTION =================
def analyze_weather():
    if not os.path.exists("weather_log.csv"):
        messagebox.showinfo("Info", "No data collected yet!")
        return

    df = pd.read_csv("weather_log.csv")

    avg_temp = round(df["Temperature"].mean(), 2)
    avg_humidity = round(df["Humidity"].mean(), 2)

    recent = df.tail(1).iloc[0]

    msg = (
        f"📊 Weather Data Insights\n\n"
        f"Average Temperature: {avg_temp}°C\n"
        f"Average Humidity: {avg_humidity}%\n\n"
        f"Most Recent Entry:\n"
        f"City: {recent['City']}\n"
        f"Temp: {recent['Temperature']}°C\n"
        f"Condition: {recent['Condition']}"
    )

    messagebox.showinfo("Weather Trends", msg)

# ================= SHOW GRAPH FUNCTION =================
def show_temp_graph():
    if not os.path.exists("weather_log.csv"):
        messagebox.showinfo("Info", "No data to plot!")
        return

    df = pd.read_csv("weather_log.csv")
    plt.figure(figsize=(6, 4))
    plt.plot(df["Date"], df["Temperature"], marker='o', color='orange', linewidth=2)
    plt.xticks(rotation=45, ha='right')
    plt.title("🌡 Temperature Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.show()

# ================= SPEAK WEATHER FUNCTION =================
def speak_weather():
    global podcast_text
    if not podcast_text:
        messagebox.showinfo("Info", "Please fetch weather first!")
        return
    try:
        file_name = "weather_podcast.mp3"
        if os.path.exists(file_name):
            os.remove(file_name)  # avoid permission denied error
        tts = gTTS(text=podcast_text, lang='en')
        tts.save(file_name)
        playsound(file_name)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to play audio.\n{e}")

# ================= GUI SETUP =================
root = tk.Tk()
root.title("🌤 Weather Broadcasting & Data Analytics App")
root.geometry("720x700")
root.resizable(False, False)

# Gradient Background
bg = Image.new("RGB", (720, 700), "#4facfe")
for y in range(700):
    r = int(79 + (0 - 79) * (y / 700))
    g = int(172 + (198 - 172) * (y / 700))
    b = int(254 + (255 - 254) * (y / 700))
    for x in range(720):
        bg.putpixel((x, y), (r, g, b))
bg = ImageTk.PhotoImage(bg)
bg_label = tk.Label(root, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Heading
heading = tk.Label(root, text="🌎 Weather Broadcasting & Data Analytics",
                   font=("Century Gothic", 22, "bold"), bg="#333333", fg="white")
heading.pack(pady=20, ipadx=10, ipady=5)

# Entry Frame
frame = tk.Frame(root, bg="#444444", bd=3)
frame.pack(pady=10)
city_entry = tk.Entry(frame, font=("Century Gothic", 16), width=25, justify='center')
city_entry.grid(row=0, column=0, ipady=5, ipadx=5, padx=5)

get_weather_button = tk.Button(frame, text="Get Weather 🌤",
                               font=("Century Gothic", 14, "bold"),
                               bg="#00C9FF", fg="black", command=get_weather)
get_weather_button.grid(row=0, column=1, padx=5)

speak_button = tk.Button(frame, text="🔊 Speak Weather",
                         font=("Century Gothic", 14, "bold"),
                         bg="#FFB800", fg="black", command=speak_weather)
speak_button.grid(row=0, column=2, padx=5)

analyze_button = tk.Button(frame, text="📊 Analyze Trends",
                           font=("Century Gothic", 14, "bold"),
                           bg="#8A2BE2", fg="white", command=analyze_weather)
analyze_button.grid(row=1, column=0, pady=10)

graph_button = tk.Button(frame, text="📈 Show Graph",
                         font=("Century Gothic", 14, "bold"),
                         bg="#00FA9A", fg="black", command=show_temp_graph)
graph_button.grid(row=1, column=1, pady=10)

city_entry.focus()

# Weather Display
weather_frame = tk.Frame(root, bg="#444444", bd=5)
weather_frame.pack(pady=20, fill='both', expand=True)
weather_label = tk.Label(weather_frame, font=("Consolas", 13),
                         bg="#444444", justify='left', fg="white")
weather_label.pack(padx=10, pady=10, anchor='w')

# Icon
icon_label = tk.Label(root, bg="#333333")
icon_label.pack(pady=10)

# Footer
footer = tk.Label(root, text="Made with ❤ by Manjot Singh",
                  font=("Century Gothic", 11), fg="white", bg="#333333")
footer.pack(side="bottom", pady=10)

root.mainloop()