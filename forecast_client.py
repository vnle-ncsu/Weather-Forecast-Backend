import requests
import configparser

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
        url = f"{self.base_url}?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,weathercode&days=7&timezone={self.timezone}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            return {"max_temp": weather_data['daily']['temperature_2m_max'][0], "min_temp": weather_data['daily']['temperature_2m_min'][0]}
        return None