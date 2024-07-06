from forecast_client import ForecastClient
from models import ForecastRequestModel, ForecastResponseModel, SevenDayForecastResponseModel, CurrentForecastModel, HourlyForecastModel


class ForecastService:
    def __init__(self):
        self.client = ForecastClient()

    def get_forecast(self, request: ForecastRequestModel) -> ForecastResponseModel:
        #geocoding service
        latitude, longitude = self.client.get_lat_long(request.zipcode)
        if latitude is None or longitude is None:
            return ForecastResponseModel(date=request.date, max_temp=0.0, min_temp=0.0, weather="", status_code=400, message="Invalid ZIP code")
        
        forecast = self.client.get_weather_forecast(latitude, longitude, request.date)
        if forecast is None:
            return ForecastResponseModel(date=request.date, max_temp=0.0, min_temp=0.0, weather="", status_code=500, message="Weather data req failed")

        return ForecastResponseModel(date=request.date, max_temp=forecast['max_temp'], min_temp=forecast['min_temp'], weather=forecast['weather'], status_code=200, message="Success")
    

    def get_7_day_forecast(self, request: ForecastRequestModel) -> SevenDayForecastResponseModel:
        latitude, longitude = self.client.get_lat_long(request.zipcode)
        if latitude is None or longitude is None:
            return SevenDayForecastResponseModel(status_code=400, message="Invalid ZIP code", forecast=[])
        
        forecast_data = self.client.get_7_day_weather_forecast(latitude, longitude)
        if forecast_data is None:
            return SevenDayForecastResponseModel(status_code=500, message="Weather data req failed", forecast=[])
        
        forecast = []
        for day in forecast_data:
            forecast.append(ForecastResponseModel(date=day['date'], max_temp=day['max_temp'], min_temp=day['min_temp'], weather=day['weather'], status_code=200, message="Success"))


        return SevenDayForecastResponseModel(status_code=200, message="Success", forecast=forecast)
    
    
    def get_current_forecast(self, request: ForecastRequestModel) -> CurrentForecastModel:
        latitude, longitude = self.client.get_lat_long(request.zipcode)
        if latitude is None or longitude is None:
            return CurrentForecastModel(temp=0.0, weather="", time="", status_code=400, message="Invalid ZIP code")
        
        current_data = self.client.get_current_weather_forecast(latitude, longitude)

        if current_data is None:
            return CurrentForecastModel(temp=0.0, weather="", time="", status_code=500, message="Weather data req failed")
        
        return CurrentForecastModel(temp=current_data['temp'], weather=current_data['weather'], time=current_data['time'], status_code=200, message="Success")
    
    
    def get_hourly_forecast(self, request: ForecastRequestModel) -> HourlyForecastModel:
        latitude, longitude = self.client.get_lat_long(request.zipcode)
        if latitude is None or longitude is None:
            return HourlyForecastModel(status_code=400, message="Invalid ZIP code", forecast=[])
        
        hourly_data = self.client.get_hourly_weather_forecast(latitude, longitude)
        if hourly_data is None:
            return HourlyForecastModel(status_code=500, message="Weather data req failed", forecast=[])

        forecast = []
        for hour in hourly_data:
            forecast.append(CurrentForecastModel(temp=hour['temp'], weather=hour['weather'], time=hour['time'], status_code=200, message="Success"))

        return HourlyForecastModel(status_code=200, message="Success", forecast=forecast)