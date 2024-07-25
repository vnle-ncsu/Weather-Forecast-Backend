# Weather-Forecast-Backend - Orange Team

## Clone Repo

_Add ssh key & what not before this_

```bash
git clone git@github.com:vnle-ncsu/Weather-Forecast-Backend.git
```

## Python Version

Running on Python 3.8.5 -> 3.8.10

## Packages you'll need

-Just use make install or look in the requirement.txt (these specefic versions because there's a lot of compatibility issues) \n
-Flask \
-requests \
-pydantic \
-flask CORs

```bash
pip install Flask
pip install requests
pip install pydantic
pip install flask-cors
```

## Makefile :)

### Install packages and dependencies

```bash
make install
```

### Clean the environment

```bash
make clean
```

### Run the backend

```bash
make run
```

### Run test (pre-req: backend has to be running)

```bash
make test
```

### Run with seeds and runs - seeds and regression testing isn't working but you can still use this command to test performance and functionality

#### Example

```bash
make test_custom RUNS=50 SEED=12345
```

### Help

```bash
make help
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

## Example cURL POST request

```bash
curl -X POST http://127.0.0.1:5000/forecast/single-day -H "Content-Type: application/json" -d '{"zipcode": "78758", "date": "2024-07-11"}'

```

or

```bash
curl -X POST http://127.0.0.1:5000/forecast/single-day -H "Content-Type: application/json" -d '{"zipcode": "78758"}'
```

For 7 day data

```bash
curl -X POST http://127.0.0.1:5000/forecast/weekly -H "Content-Type: application/json" -d '{"zipcode": "78758"}'
```

For current weather/
route: /forecast/<zipcode>

```bash
curl -X GET http://127.0.0.1:5000/forecast/78758
```

For hourly forecast

```bash
curl -X POST http://127.0.0.1:5000/forecast/hourly -H "Content-Type: application/json" -d '{"zipcode": "78758"}'
```

For more information on forecast endpoints go to ./docs/forecast.txt
