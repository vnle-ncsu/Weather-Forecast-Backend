# Weather-Forecast-Backend

Clone Repo \

packages you'll need \
-Flask (pip install Flask) \
-requests (pip install requests) \
-pydantic (pip install pydantic) \

Running on Python 3.8.5 \

Probably should create a virtual env to run this on \
python3 -m venv venv \
source venv/bin/activate \
pip install -r requirements.txt \
python3 app.py \
deactivate \

Example curl post req \
curl -X POST http://127.0.0.1:5000/get_weather -H "Content-Type: application/json" -d '{"zipcode": "78758", "date": "2024-06-27"}' \
