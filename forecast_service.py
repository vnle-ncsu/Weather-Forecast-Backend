from forecast_client import ForecastClient
from models import ForecastRequestModel, ForecastResponseModel


class ForecastService:
    def __init__(self):
        self.client = ForecastClient()

    def get_forecast(self, request: ForecastRequestModel) -> ForecastResponseModel:
        #geocoding service
        latitude, longitude = self.client.get_lat_long(request.zipcode)
        if latitude is None or longitude is None:
            return ForecastResponseModel(date=request.date, max_temp=0.0, min_temp=0.0, status_code=400, message="Invalid ZIP code")
        
        forecast = self.client.get_weather_forecast(latitude, longitude, request.date)
        if forecast is None:
            return ForecastResponseModel(date=request.date, max_temp=0.0, min_temp=0.0, status_code=500, message="Weather data req failed")

        return ForecastResponseModel(date=request.date, max_temp=forecast['max_temp'], min_temp=forecast['min_temp'], status_code=200, message="Success")
    

    def get_7_day_forecast(self, request: ForecastRequestModel) -> dict:
        return None
    