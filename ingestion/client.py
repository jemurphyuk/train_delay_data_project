import requests
from config import Config

class TflClient:
    def __init__(self, app_key: str = None, api_secret: str = None):
        self.app_key = app_key or Config.APP_KEY
        self.base_url = Config.BASE_URL
        # print(self.app_key)
        # print(len(self.app_key))
        
    def _params(self):
        """
        Authentitcation paramters
        """
        return {
            "app_key": self.app_key,
        }
    

    def _get(self, endpoint: str):
        """
        Internal helper for GET requests.
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=self._params(), timeout=10)

        if response.status_code != 200:
            raise Exception(
                f"TfL API error {response.status_code}: {response.text}"
            )

        return response.json()


    def get_line_status(self, line_id: str):
        """
        Fetch the current status for a given line.
        Example: /Line/victoria/Status
        """
        endpoint = f"/Line/{line_id}/Status"
        return self._get(endpoint)

    def get_line_disruptions(self, line_id: str):
        """
        Fetch disruptions for a given line.
        Example: /Line/victoria/Disruption
        """
        endpoint = f"/Line/{line_id}/Disruption"
        return self._get(endpoint)

    def get_line_arrivals(self, line_id: str):
        """
        Fetch real-time arrival predictions for a line.
        Example: /Line/victoria/Arrivals
        """
        endpoint = f"/Line/{line_id}/Arrivals"
        return self._get(endpoint)

    def get_stoppoint_arrivals(self, stop_id: str):
        """
        Fetch arrivals for a specific station/stop.
        Example: /StopPoint/940GZZLUBND/Arrivals
        """
        endpoint = f"/StopPoint/{stop_id}/Arrivals"
        return self._get(endpoint)
