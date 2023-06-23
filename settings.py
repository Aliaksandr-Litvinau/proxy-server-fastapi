from decouple import config
from pydantic import BaseSettings


class Settings(BaseSettings):
    base_url: str = config('BASE_URL', default='https://blackrussia.online')
    status_ok_list: list[int] = list(
        map(int, config('STATUS_OK_LIST',
                        default='200,201,203,204,205,206,207,208,226,300,301,302,303,304,305,306,307,308').split(',')))

    class Config:
        env_file = '.env'


settings = Settings()
