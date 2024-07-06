import requests
import configparser
from weather_codes import WEATHER_CODES
from datetime import datetime

class ForecastClient:
    def __init__(self):
        #load config
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.base_url = self.config['WEATHER_API']['base_url']
        self.timezone = self.config['WEATHER_API']['timezone']

    def get_lat_long(self, zip_code: str):
        url = f"http://api.zippopotam.us/us/{zip_code}"
        response = requests.get(url)
        if response.status_code == 200:
            location_data = response.json()
            latitude = float(location_data['places'][0]['latitude'])
            longitude = float(location_data['places'][0]['longitude'])
            return latitude, longitude
        return None, None

    def get_weather_forecast(self, latitude: float, longitude: float, date: str):
        #date format xxxx-xx-xx, year-month-day
        #https://open-meteo.com/en/docs
        #under "Daily Parameter Definition", requesting max and min daily air temp, weather code
        #this is just for a single day but you can get api response of 7 day forecast as well
        #url = f"{self.base_url}?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,weathercode&days=7&timezone={self.timezone}"
        url = f"{self.base_url}?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,weathercode&start={date}&end={date}&temperature_unit=fahrenheit&timezone={self.timezone}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            weather_code = weather_data['daily']['weathercode'][0]
            weather_description = WEATHER_CODES.get(weather_code, "Unknown")
            return {"max_temp": weather_data['daily']['temperature_2m_max'][0], "min_temp": weather_data['daily']['temperature_2m_min'][0],"weather": weather_description}
        return None
    
    def get_7_day_weather_forecast(self, latitude: float, longitude: float):
        url = f"{self.base_url}?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,weathercode&temperature_unit=fahrenheit&timezone={self.timezone}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            forecast = []
            for i in range(0,7):
                weather_code = weather_data['daily']['weathercode'][i]
                weather_description = WEATHER_CODES.get(weather_code, "Unknown")
                day_forecast = {"date": weather_data['daily']['time'][i], "max_temp": weather_data['daily']['temperature_2m_max'][i], "min_temp": weather_data['daily']['temperature_2m_min'][i], "weather": weather_description}
                forecast.append(day_forecast)
            return forecast
        return None
    
    def get_current_weather_forecast(self, latitude: float, longitude: float):
        url = f"{self.base_url}?latitude={latitude}&longitude={longitude}&current=temperature_2m,weathercode&temperature_unit=fahrenheit&timezone={self.timezone}"
        #print(url)
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            weather_code = weather_data['current']['weathercode']
            weather_description = WEATHER_CODES.get(weather_code, "Unknown")
            return {"temp": weather_data['current']['temperature_2m'], "weather": weather_description, "time":str(datetime.now())}
        return None
    
    def get_hourly_weather_forecast(self, latitude: float, longitude: float):
        url = f"{self.base_url}?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,weathercode&temperature_unit=fahrenheit&forecast_days=1&timezone={self.timezone}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            hourly_forecast = []
            if 'hourly' in weather_data:
                for i in range(len(weather_data['hourly']['temperature_2m'])):
                    weather_code = weather_data['hourly']['weathercode'][i]
                    weather_description = WEATHER_CODES.get(weather_code, "Unknown")
                    hour_forecast = {"temp": weather_data['hourly']['temperature_2m'][i], "weather": weather_description, "time": weather_data['hourly']['time'][i]}
                    hourly_forecast.append(hour_forecast)
            return hourly_forecast
        return None