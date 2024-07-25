from forecast_client import ForecastClient
from models import ForecastRequestModel, ForecastResponseModel, SevenDayForecastResponseModel, CurrentForecastModel, HourlyForecastModel, RatingRequestModel, RatingResponseModel
import tensorflow as tf
import numpy as np
import joblib


class ForecastService:
    def __init__(self):
        self.client = ForecastClient()
        self.activity_model = self.load_activity_model()
        #self.activity_mapping = {'golf': 0, 'hiking': 1, 'running': 2}

    def get_forecast(self, request: ForecastRequestModel) -> ForecastResponseModel:
        #geocoding service
        latitude, longitude = self.client.get_lat_long(request.zipcode)
        if latitude is None or longitude is None:
            return ForecastResponseModel(date=request.date, max_temp=0.0, min_temp=0.0, weather="", status_code=400, message="Invalid ZIP code")
        
        forecast = self.client.get_daily_weather_forecast(latitude, longitude, request.date)
        if forecast is None:
            return ForecastResponseModel(date=request.date, max_temp=0.0, min_temp=0.0, weather="", status_code=500, message="Weather data req failed")

        return forecast
    

    def get_7_day_forecast(self, request: ForecastRequestModel) -> SevenDayForecastResponseModel:
        latitude, longitude = self.client.get_lat_long(request.zipcode)
        if latitude is None or longitude is None:
            return SevenDayForecastResponseModel(status_code=400, message="Invalid ZIP code", forecast=[])
        
        forecast_data = self.client.get_7_day_weather_forecast(latitude, longitude)
        if forecast_data is None:
            return SevenDayForecastResponseModel(status_code=500, message="Weather data req failed", forecast=[])

        return SevenDayForecastResponseModel(status_code=200, message="Success", forecast=forecast_data)
    
    
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
        return HourlyForecastModel(status_code=200, message="Success", forecast=hourly_data)
    
    def load_activity_model(self):
        interpreter = tf.lite.Interpreter(model_path="activity_suitability_model.tflite")
        interpreter.allocate_tensors()
        return interpreter

    def get_activity_suitability(self, request: RatingRequestModel) -> int:
        scaler = joblib.load('scaler.joblib')
        activity_mapping = {'golf': 1, 'hiking': 2, 'running': 3}
        
        
        input_data_activity = activity_mapping[request.activity]

        input_details = self.activity_model.get_input_details()
        output_details = self.activity_model.get_output_details()

        #print("Input details:", input_details)

        #activity_encoded = np.array([request.activity.encode('utf-8')], dtype=np.string_)
        print(type(input_data_activity))
        numerical_inputs = np.array([[input_data_activity, request.temp_max, request.precipitation, request.temp_min, request.weather_code]], dtype=np.float32)
        #for i in numerical_inputs:
        #    print(type(i))
        input_scaled = scaler.transform(numerical_inputs)
        #for iss in input_scaled:
        #    print(type(iss))
        self.activity_model.set_tensor(input_details[0]['index'], input_scaled)


        #for input_detail in input_details:
        #    if input_detail['dtype'] == np.string_:
        #        self.activity_model.set_tensor(input_detail['index'], activity_encoded)
        #    elif input_detail['dtype'] == np.float32:
        #        self.activity_model.set_tensor(input_detail['index'], numerical_inputs)

        self.activity_model.invoke()
        y_pred = self.activity_model.get_tensor(output_details[0]['index'])[0]
        y_pred_rounded = np.clip(np.round(y_pred), 1, 5)

        return int(y_pred_rounded)