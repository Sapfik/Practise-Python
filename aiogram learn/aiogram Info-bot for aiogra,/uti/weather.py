import pyowm
from config import OWM_KEY

owm = pyowm.OWM(OWM_KEY)

def get_forecast(place):
    observation = owm.weather_manager().weather_at_place(place)
    weather = observation.weather
    temperature = weather.temperature('celsius')["temp"]
    wind = weather.wind()['speed']
    clouds = weather.clouds
    humidity = weather.humidity
    forecast = f"🏙  In {place} is currently {weather.detailed_status} \n🌡️ {temperature} °C \n💨 {wind} m/s \n🌫️  {clouds} % \n💦 {humidity} %"
    return forecast

