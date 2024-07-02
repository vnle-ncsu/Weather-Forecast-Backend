from flask import Flask, request, jsonify
from forecast_service import ForecastService
from models import ForecastRequestModel
#from pydantic import ValidationError

app = Flask(__name__)

forecast_service = ForecastService()

@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    request_model = ForecastRequestModel(**data) #have to unpack data apparently for pydantic model
    #except ValidationError as e:
    #   return jsonify(e.errors()), 400
    
    response = forecast_service.get_forecast(request_model)
    return jsonify(response.dict()), response.status_code


if __name__ == '__main__':
    app.run(debug=True)


