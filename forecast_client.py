import requests
import configparser
from weather_codes import WEATHER_CODES
from datetime import datetime
from models import ForecastResponseModel, CurrentForecastModel

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

    def get_daily_weather_forecast(self, latitude: float, longitude: float, date: str):
        #date format xxxx-xx-xx, year-month-day
        #https://open-meteo.com/en/docs
        #under "Daily Parameter Definition", requesting max and min daily air temp, weather code
        #this is just for a single day but you can get api response of 7 day forecast as well
        #url = f"{self.base_url}?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,weathercode&days=7&timezone={self.timezone}"
        url = f"{self.base_url}?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,weathercode,uv_index_max,sunrise,wind_speed_10m_max,wind_direction_10m_dominant,sunset,precipitation_sum,precipitation_probability_max,rain_sum,showers_sum,snowfall_sum&start_date={date}&end_date={date}&temperature_unit=fahrenheit&timezone={self.timezone}"
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            weather_code = weather_data['daily']['weathercode'][0]
            weather_description = WEATHER_CODES.get(weather_code, "Unknown")
            day_forecast = ForecastResponseModel(
                date = weather_data['daily']['time'] [0],
                max_temp = weather_data['daily']['temperature_2m_max'] [0],
                min_temp = weather_data['daily']['temperature_2m_min'] [0],
                max_apparent_temp=weather_data['daily']['apparent_temperature_max'] [0],
                min_apparent_temp=weather_data['daily']['apparent_temperature_min'] [0],
                uv_index=weather_data['daily']['uv_index_max'] [0],
                max_wind_speed=weather_data['daily']['wind_speed_10m_max'] [0],
                dominant_wind_direction=weather_data['daily']['wind_direction_10m_dominant'] [0],
                weather = weather_description,
                sunrise =weather_data['daily']['sunrise'] [0],
                sunset = weather_data['daily']['sunset'] [0],
                precip_sum = weather_data['daily']['precipitation_sum'] [0],
                precip_prob = weather_data['daily']['precipitation_probability_max'] [0],
                rain_sum = (weather_data['daily']['rain_sum'] + weather_data['daily']['showers_sum']) [0],
                snowfall_sum = weather_data['daily']['snowfall_sum'] [0],
                message = 'success',
                status_code = 200
            )
            return day_forecast
        return None
    
    def get_7_day_weather_forecast(self, latitude: float, longitude: float):
        url = f"{self.base_url}?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,weathercode,uv_index_max,sunrise,wind_speed_10m_max,wind_direction_10m_dominant,sunset,precipitation_sum,precipitation_probability_max,rain_sum,showers_sum,snowfall_sum&wind_speed_unit=mph&precipitation_unit=inch&temperature_unit=fahrenheit&timezone={self.timezone}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            forecast = []
            for i in range(0,7):
                weather_code = weather_data['daily']['weathercode'][i]
                weather_description = WEATHER_CODES.get(weather_code, "Unknown")
                day_forecast = ForecastResponseModel(
                    date = weather_data['daily']['time'][i],
                    max_temp = weather_data['daily']['temperature_2m_max'][i],
                    min_temp = weather_data['daily']['temperature_2m_min'][i],
                    max_apparent_temp=weather_data['daily']['apparent_temperature_max'][i],
                    min_apparent_temp=weather_data['daily']['apparent_temperature_min'][i],
                    uv_index=weather_data['daily']['uv_index_max'][i],
                    max_wind_speed=weather_data['daily']['wind_speed_10m_max'][i],
                    dominant_wind_direction=weather_data['daily']['wind_direction_10m_dominant'][i],
                    weather = weather_description,
                    sunrise =weather_data['daily']['sunrise'][i],
                    sunset = weather_data['daily']['sunset'][i],
                    precip_sum = weather_data['daily']['precipitation_sum'][i],
                    precip_prob = weather_data['daily']['precipitation_probability_max'][i],
                    rain_sum = (weather_data['daily']['rain_sum'][i] + weather_data['daily']['showers_sum'][i]),
                    snowfall_sum = weather_data['daily']['snowfall_sum'][i],
                    message = 'success',
                    status_code = 200
                )
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
        url = f"{self.base_url}?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,weathercode,apparent_temperature,precipitation_probability,rain,showers,snowfall,wind_speed_10m,wind_direction_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&forecast_days=1&timezone={self.timezone}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            hourly_forecast = []
            if 'hourly' in weather_data:
                for i in range(len(weather_data['hourly']['temperature_2m'])):
                    weather_code = weather_data['hourly']['weathercode'][i]
                    weather_description = WEATHER_CODES.get(weather_code, "Unknown")
                    hour_forecast = CurrentForecastModel( 
                        temp = weather_data['hourly']['temperature_2m'][i],
                        apparent_temp = weather_data['hourly']['apparent_temperature'][i],
                        precip_prob = weather_data['hourly']['precipitation_probability'][i],
                        rain = (weather_data['hourly']['rain'][i] + weather_data['hourly']['showers'][i]),
                        snow = weather_data['hourly']['snowfall'][i],
                        wind_speed = weather_data['hourly']['wind_speed_10m'][i],
                        wind_direction = weather_data['hourly']['wind_direction_10m'][i],
                        weather = weather_description,
                        time = weather_data['hourly']['time'][i],
                        status_code=200,
                        message='success'
                    )
                    hourly_forecast.append(hour_forecast)
            return hourly_forecast
        return None