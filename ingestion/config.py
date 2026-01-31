import os
from dataclasses import dataclass

@dataclass
class Config:
    APP_KEY: str = os.getenv("TFL_APP_KEY")
    BASE_URL: str = "https://api.tfl.gov.uk"
    DEFAULT_LINE: str = "victoria" # Victoria Line
    DEFAULT_STATION: str = "940GZZLUBND"  # Bond Street
    DB_HOST: str = "localhost"
    DB_USER: str = os.getenv("LOCAL_HOST_USER")
    DB_PASSWORD: str = os.getenv("LOCAL_HOST_PASSWORD")
    DB_NAME: str = "train_data"