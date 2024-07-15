import unittest
import requests
import time
import random
import sys
import argparse
from datetime import datetime, timedelta
import random_address
import xmlrunner

class TestWeatherForecastAPIPerformance(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"
    SEED = 42  # Default seed
    NUM_RUNS = 10  # Default number of runs

    STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
              'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
              'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

    @classmethod
    def setUpClass(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument('num_runs', type=int, nargs='?', default=cls.NUM_RUNS, help='Number of test runs')
        parser.add_argument('seed', type=int, nargs='?', default=cls.SEED, help='Random seed value')
        args = parser.parse_args()

        cls.NUM_RUNS = args.num_runs
        cls.SEED = args.seed
        random.seed(cls.SEED)

        log_file_name = f'./results/test_results_{cls.SEED}.log'
        cls.log_file =open(log_file_name, 'w')
        cls.log_file.write(f"Test run with SEED={cls.SEED}, NUM_RUNS={cls.NUM_RUNS}\n")

    @classmethod
    def tearDownClass(cls):
        cls.log_file.close()

    def generate_random_zip_code(self):
        address = {}
        while not address or 'postalCode' not in address:
            state = random.choice(self.STATES)
            address = random_address.real_random_address_by_state(state)
            # print(f"Retrying... Generated address: {address}") 

        return address['postalCode']

    def generate_random_date(self):
        start_date = datetime.now()
        end_date = start_date + timedelta(days=7)
        random_date = start_date + (end_date - start_date) * random.random()
        return random_date.strftime('%Y-%m-%d')

    def log_result(self, endpoint, zipcode, date, duration, status_code):
        self.log_file.write(f"Endpoint: {endpoint}, ZIP code: {zipcode}, Date: {date}, Duration: {duration:.2f}s, Status code: {status_code}\n")

    def test_get_current_forecast_performance(self):
        for _ in range(self.NUM_RUNS):
            zipcode = self.generate_random_zip_code()
            url = f"{self.BASE_URL}/forecast/{zipcode}"
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            duration = end_time - start_time

            self.assertEqual(response.status_code, 200, f"Invalid response for ZIP code {zipcode}")
            self.assertLess(duration, 2, f"Performance test failed: {duration} seconds for ZIP code {zipcode}")
            self.log_result('/forecast', zipcode, None, duration, response.status_code)

    def test_get_single_day_forecast_performance(self):
        for _ in range(self.NUM_RUNS):
            zipcode = self.generate_random_zip_code()
            date = self.generate_random_date()
            url = f"{self.BASE_URL}/forecast/single-day"
            data = {"zipcode": zipcode,"date": date}
            start_time = time.time()
            response = requests.post(url, json=data)
            end_time = time.time()
            duration = end_time - start_time

            self.assertEqual(response.status_code, 200, f"Invalid response for ZIP code {zipcode} and date {date}")
            self.assertLess(duration, 2, f"Performance test failed: {duration} seconds for ZIP code {zipcode} and date {date}")
            self.log_result('/forecast/single-day', zipcode, date, duration, response.status_code)

    def test_get_weekly_forecast_performance(self):
        for _ in range(self.NUM_RUNS):
            zipcode = self.generate_random_zip_code()
            url = f"{self.BASE_URL}/forecast/weekly"
            data = {"zipcode": zipcode}
            start_time = time.time()
            response = requests.post(url, json=data)
            end_time = time.time()
            duration = end_time - start_time

            self.assertEqual(response.status_code, 200, f"Invalid response for ZIP code {zipcode}")
            self.assertLess(duration, 2, f"Performance test failed: {duration} seconds for ZIP code {zipcode}")
            self.log_result('/forecast/weekly', zipcode, None, duration, response.status_code)

    def test_get_hourly_forecast_performance(self):
        for _ in range(self.NUM_RUNS):
            zipcode = self.generate_random_zip_code()
            url = f"{self.BASE_URL}/forecast/hourly"
            data = {"zipcode": zipcode}
            start_time = time.time()
            response = requests.post(url, json=data)
            end_time = time.time()
            duration = end_time - start_time

            self.assertEqual(response.status_code, 200, f"Invalid response for ZIP code {zipcode}")
            self.assertLess(duration, 2, f"Performance test failed: {duration} seconds for ZIP code {zipcode}")
            self.log_result('/forecast/hourly', zipcode, None, duration, response.status_code)



## Functionality test, invalid inputs
class TestWeatherForecastAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"

    @classmethod
    def setUpClass(cls):
        cls.log_file_name = './results/test_invalid_data.log'
        cls.log_file = open(cls.log_file_name, 'w')

    @classmethod
    def tearDownClass(cls):
        cls.log_file.close()

    def log_result(self, endpoint, data, status_code):
        self.log_file.write(f"Endpoint: {endpoint}, Data: {data}, Status code: {status_code}\n")

    def test_invalid_zip_code(self):
        invalid_zip = "00000"
        url = f"{self.BASE_URL}/forecast/{invalid_zip}"
        response = requests.get(url)
        self.log_result('/forecast', {'zipcode': invalid_zip}, response.status_code)
        self.assertEqual(response.status_code, 400, "Expected status code 400 for invalid ZIP code")

    def test_invalid_date(self):
        valid_zip = "90210"  # Example of a valid ZIP code
        invalid_date = "2024-02-30"  # Invalid date
        url = f"{self.BASE_URL}/forecast/single-day"
        data = {"zipcode": valid_zip,"date": invalid_date}
        response = requests.post(url, json=data)
        self.log_result('/forecast/single-day', data, response.status_code)
        self.assertEqual(response.status_code, 400, "Expected status code 400 for invalid date")

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='./results'), argv=[sys.argv[0]])
