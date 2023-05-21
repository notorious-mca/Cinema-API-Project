#config.py

import os

class Settings:
    PROJECT_NAME:str = "Cinema API"
    PROJECT_VERSION: str = "1.0.0"

    SECRET_KEY :str = "cinQUEDa45?"
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins

settings = Settings()