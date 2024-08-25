from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ResortHoliday(BaseModel):
    url: str = 'https://resort-holiday.com/api/'


class TelegramBot(BaseModel):
    token: str


class Settings(BaseSettings):
    bot: TelegramBot

    resort_holiday: ResortHoliday = ResortHoliday()

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__'
    )


settings = Settings()
