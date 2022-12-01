import requests, json

def KelvinToCelsius(temp):
    return round(temp - 273.15,2)

def get_weather(loc):
    my_api_key = "135dec65c14a354d6047c99b13533fe5"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={loc}&appid={my_api_key}&units=metric"
    res = requests.get(url)
    data = res.json()
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind = data['wind']['speed']
    description = data['weather'][0]['description']
    temp = data['main']['temp']

    return f"`Temperature: {temp} °C`\n`Wind: {wind}`\n`Pressure: {pressure} Pa`\n`Humidity: {humidity}%`\n`Description: {description}`"
