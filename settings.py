from decouple import config
from pydantic import BaseSettings


class Settings(BaseSettings):
    base_url: str = config('BASE_URL', default='https://blackrussia.online')

    class Config:
        env_file = '.env'


settings = Settings()
