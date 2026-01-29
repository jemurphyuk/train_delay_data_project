import requests
from config import Config

class NationalRailClient:
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or Config.API_KEY
        self.api_secret = api_secret or Config.API_SECRET
        self.base_url = Config.BASE_URL

    def _headers(self):
        return {
            "x-apikey": self.api_key,
            "x-apisecret": self.api_secret,
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