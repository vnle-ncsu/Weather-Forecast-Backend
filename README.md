# Weather-Forecast-Backend

## Clone Repo

_Add ssh key & what not before this_

```bash
git clone git@github.com:vnle-ncsu/Weather-Forecast-Backend.git\
```

## Python Version

Running on Python 3.8.5

## Packages you'll need

-Flask \
-requests \
-pydantic

```bash
pip install Flask
pip install requests
pip install pydantic
```

## Running in Virtual Environment

Step to Run on Virtual Env

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

To leave venv

```bash
deactivate
```

## Required Packages

To update requirements.txt

```bash
python3 -m  pipreqs.pipreqs . --force
```

## Example curl post req

```bash
curl -X POST http://127.0.0.1:5000/get_weather -H "Content-Type: application/json" -d '{"zipcode": "78758", "date": "2024-06-27"}'
```

or\

```bash
curl -X POST http://127.0.0.1:5000/get_weather -H "Content-Type: application/json" -d '{"zipcode": "78758"}'
```

For more information on forecast endpoints go to ./docs/forecast.txt
