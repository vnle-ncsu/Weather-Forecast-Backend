from flask import Flask, request, jsonify
from forecast_service import ForecastService
from models import ForecastRequestModel
from datetime import datetime
#from pydantic import ValidationError

app = Flask(__name__)

forecast_service = ForecastService()

@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    #Use Today's date if date isn't given
    if 'date' not in data or not data['date']:
        data['date'] = datetime.now().strftime('%Y-%m-%d')
    request_model = ForecastRequestModel(**data) #have to unpack data apparently for pydantic model
    #except ValidationError as e:
    #   return jsonify(e.errors()), 400
    
    response = forecast_service.get_forecast(request_model)
    return jsonify(response.dict()), response.status_code

@app.route('/get_7_day_forecast', methods=['POST'])
def get_7_day_forecast():
    data = request.get_json()

    if 'date' not in data or not data['date']:
        data['date'] = datetime.now().strftime('%Y-%m-%d')
    
    request_model = ForecastRequestModel(**data) 
    #except ValidationError as e:
    #   return jsonify(e.errors()), 400
    response = forecast_service.get_7_day_forecast(request_model)
    return jsonify(response.dict()), response.status_code

@app.route('/get_current_forecast', methods=['POST'])
def get_current_forecast():
    data = request.get_json()

    if 'date' not in data or not data['date']:
        data['date'] = datetime.now().strftime('%Y-%m-%d')
    
    request_model = ForecastRequestModel(**data) 
    #except ValidationError as e:
    #   return jsonify(e.errors()), 400
    response = forecast_service.get_current_forecast(request_model)
    return jsonify(response.dict()), response.status_code


@app.route('/get_hourly_forecast', methods=['POST'])
def get_hourly_forecast():
    data = request.get_json()

    if 'date' not in data or not data['date']:
        data['date'] = datetime.now().strftime('%Y-%m-%d')
    
    request_model = ForecastRequestModel(**data) 
    #except ValidationError as e:
    #   return jsonify(e.errors()), 400
    response = forecast_service.get_hourly_forecast(request_model)
    return jsonify(response.dict()), response.status_code

if __name__ == '__main__':
    app.run(debug=True)


