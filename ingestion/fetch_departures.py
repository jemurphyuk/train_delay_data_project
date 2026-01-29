from client import NationalRailClient
from storage import RawStorage
from config import Config

class DepartureIngestion:
    def __init__(self, station_code: str = None):
        self.station_code = station_code or Config.DEFAULT_STATION
        self.client = NationalRailClient()
        self.storage = RawStorage()

    def run(self):
        endpoint = f"departures/{self.station_code}"
        data = self.client.get(endpoint)
        self.storage.save_departures(self.station_code, data)
        return data