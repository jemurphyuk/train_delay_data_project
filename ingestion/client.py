import requests
from .config import config

class NationalRailClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.API_KEY
        self.base_url = config.BASE_URL

    def _headers(self):
        return {
            "x-apikey": self.api_key,
            "Content-Type": "application/json"
        }

    def get(self, endpoint: str):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self._headers())

        if response.status_code != 200:
            raise Exception(
                f"API error {response.status_code}: {response.text}"
            )

        return response.json()