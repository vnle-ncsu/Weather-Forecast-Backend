from pydantic import BaseModel
from typing import Optional
from typing import List, Dict

class ForeRequestModel(BaseModel):
    zipcode: int
    date: List[str]
    activity: str

class ForecastRequestModel(BaseModel):
    zipcode: int
    date: str

class ForecastResponseModel(BaseModel):
    date: str
    max_temp: float
    min_temp: float
    max_apparent_temp: float
    min_apparent_temp: float
    weather: str
    sunrise: Optional[str] = None
    sunset: Optional[str] = None
    uv_index: Optional[float] = None
    max_wind_speed: Optional[float] = None
    dominant_wind_direction: Optional[int] = None
    precip_sum: Optional[float] = None
    precip_prob: Optional[float] = None
    rain_sum: Optional[float] = None
    snow_sum: Optional[float] = None
    status_code: int
    message: str
    rating: Optional[int] = None

class SevenDayForecastResponseModel(BaseModel):
    status_code: int
    message: str
    forecast: List[ForecastResponseModel]

class CurrentForecastModel(BaseModel):
    temp: float
    apparent_temp: float
    precip_prob: Optional[float] = None
    rain: Optional[float] = None
    snow: Optional[float] = None
    weather: str
    wind_speed: Optional[float] = None
    wind_direction: Optional[int] = None
    time: str
    status_code: int
    message: str

class HourlyForecastModel(BaseModel):
    status_code: int
    message: str
    forecast: List[CurrentForecastModel]
    ratings: Optional[List[int]] = None

    