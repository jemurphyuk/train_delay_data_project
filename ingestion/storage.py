import json
import mysql.connector
from datetime import datetime, timezone

class RawStorage:
    def __init__(
        self,
        host="localhost",
        user="root",
        password="password",
        database="train_data"
    ):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_departures (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ingested_at DATETIME,
                station_code VARCHAR(10),
                payload JSON
            )
        """)
        self.conn.commit()

    def save_departures(self, station_code: str, payload: dict):
        query = """
            INSERT INTO raw_departures (ingested_at, station_code, payload)
            VALUES (%s, %s, %s)
        """
        values = (
            datetime.now(timezone.utc),
            station_code,
            json.dumps(payload)
        )

        self.cursor.execute(query, values)
        self.conn.commit()