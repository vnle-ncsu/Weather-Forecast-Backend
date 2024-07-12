from flask import Flask, request, jsonify
from flask_cors import CORS
from forecast_service import ForecastService
from models import ForecastRequestModel
from datetime import datetime
from pydantic import ValidationError

app = Flask(__name__)
CORS(app)

forecast_service = ForecastService()

@app.route('/forecast/single-day', methods=['POST'])
def get_weather():
    data = request.get_json()
    try:
        request_model = ForecastRequestModel(**data)
        datetime.strptime(request_model.date, '%Y-%m-%d')  # Date validation
    except (ValidationError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    try: 
         #Use Today's date if date isn't given
        if 'date' not in data or not data['date']:
            data['date'] = datetime.now().strftime('%Y-%m-%d')
        request_model = ForecastRequestModel(**data) #have to unpack data apparently for pydantic model
    except ValidationError as e:
       return jsonify(e.errors()), 400
    
    response = forecast_service.get_forecast(request_model)
    return jsonify(response.dict()), response.status_code

@app.route('/forecast/weekly', methods=['POST'])
def get_7_day_forecast():
    try: 
        data = request.get_json()
         #Use Today's date if date isn't given
        if 'date' not in data or not data['date']:
            data['date'] = datetime.now().strftime('%Y-%m-%d')
        request_model = ForecastRequestModel(**data) 
    except ValidationError as e:
       return jsonify(e.errors()), 400
    
    response = forecast_service.get_7_day_forecast(request_model)
    return jsonify(response.dict()), response.status_code

@app.route('/forecast/<string:zipcode>', methods=['GET'])
def get_current_forecast(zipcode):
    data = {'zipcode': zipcode}
    if 'date' not in data or not data['date']:
        data['date'] = datetime.now().strftime('%Y-%m-%d')
    try:
        request_model = ForecastRequestModel(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
    response = forecast_service.get_current_forecast(request_model)
    return jsonify(response.dict()), response.status_code


@app.route('/forecast/hourly', methods=['POST'])
def get_hourly_forecast():
    try: 
        data = request.get_json()
         #Use Today's date if date isn't given
        if 'date' not in data or not data['date']:
            data['date'] = datetime.now().strftime('%Y-%m-%d')
        request_model = ForecastRequestModel(**data) 
    except ValidationError as e:
       return jsonify(e.errors()), 400
    response = forecast_service.get_hourly_forecast(request_model)
    return jsonify(response.dict()), response.status_code

@app.route('/geocode/<string:zipcode>', methods=['GET'])
def get_geocode(zipcode):
    data = {'zipcode': zipcode}
    if 'date' not in data or not data['date']:
        data['date'] = datetime.now().strftime('%Y-%m-%d')
    try:
        request_model = ForecastRequestModel(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
    response = forecast_service.get_geocode(request_model)
    return jsonify(response.dict()), response.status_code

if __name__ == '__main__':
    app.run(debug=True)


