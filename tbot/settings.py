from pydantic import BaseModel
from pydantic_settings import BaseSettings


class ResortHoliday(BaseModel):
    url: str = 'https://resort-holiday.com/api/'


class Settings(BaseSettings):
    resort_holiday: ResortHoliday


settings = Settings()
