from pydantic import BaseSettings, SecretStr
from typing import List
    

class Settings(BaseSettings):
    bot_token: SecretStr
    admin_ids: List[int]

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

config = Settings()