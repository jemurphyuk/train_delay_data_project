import utils
from datetime import datetime
from client import TflClient
from storage import RawDatabase
from config import Config

class TflIngestion:
    """
    Ingests TfL line status and arrival predictions into MySQL.
    This mirrors the structure of your old National Rail ingestion pipeline.
    """

    def __init__(self):
        self.client = TflClient()
        self.db = RawDatabase()

    # ---------------------------------------------------------
    # Line Status Ingestion
    # ---------------------------------------------------------

    def ingest_line_status(self, line_id: str):
        """
        Fetches the current status for a line and stores it in MySQL.
        """
        print(f"[INFO] Fetching line status for {line_id}")

        data = self.client.get_line_status(line_id)

        # TfL returns a list of statuses
        for entry in data:
            for status in entry.get("lineStatuses", []):
                record = {
                    "line_id": entry.get("id"),
                    "status_severity": status.get("statusSeverity"),
                    "status_description": status.get("statusSeverityDescription"),
                    "reason": status.get("reason"),
                    "timestamp": datetime.now(),
                }

                self.db.insert("tfl_line_status_raw", record)

        print(f"[SUCCESS] Line status ingested for {line_id}")

    # ---------------------------------------------------------
    # Line Arrivals Ingestion
    # ---------------------------------------------------------

    def ingest_line_arrivals(self, line_id: str):
        """
        Fetches real-time arrival predictions for a line and stores them.
        """
        print(f"[INFO] Fetching arrivals for {line_id}")

        arrivals = self.client.get_line_arrivals(line_id)

        for a in arrivals:
            record = {
                "line_id": a.get("lineId"),
                "station_id": a.get("naptanId"),
                "platform": a.get("platformName"),
                "expected_arrival": utils.parse_tfl_datetime(a.get("expectedArrival")),
                "time_to_station": a.get("timeToStation"),
                "current_location": a.get("currentLocation"),
                "timestamp": datetime.now(),
            }

            self.db.insert("tfl_arrivals_raw", record)

        print(f"[SUCCESS] Arrivals ingested for {line_id}")

    # ---------------------------------------------------------
    # Combined ingestion (for Airflow or run.py)
    # ---------------------------------------------------------

    def ingest_all(self, line_id: str = None):
        """
        Runs both ingestion steps for a given line.
        """
        line_id = line_id or Config.DEFAULT_LINE

        self.ingest_line_status(line_id)
        self.ingest_line_arrivals(line_id)