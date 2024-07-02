from pydantic import BaseModel
from typing import List, Dict

class ForecastRequestModel(BaseModel):
    zipcode: int
    date: str

class ForecastResponseModel(BaseModel):
    date: str
    max_temp: float
    min_temp: float
    status_code: int
    message: str

class SevenDayForecastResponseModel(BaseModel):
    status_code: int
    message: str
    forecast: List[ForecastResponseModel]