import os
from dataclasses import dataclass

@dataclass
class Config:
    API_KEY: str = os.getenv("NR_API_KEY")
    API_SECRET: str = os.getenv("NR_API_SECRET")
    BASE_URL: str = "https://api1.raildata.org.uk/ldb/v1"
    DEFAULT_STATION: str = "LST"  # Liverpool Street