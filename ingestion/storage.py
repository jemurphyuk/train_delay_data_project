import mysql.connector
from mysql.connector import Error
from config import Config


class RawDatabase:
    """
    MySQL wrapper for inserting TfL raw data.
    Matches the structure of your existing project.
    """

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("[DB] Connected to MySQL")

        except Error as e:
            raise Exception(f"[DB ERROR] Could not connect: {e}")


    def insert(self, table: str, data: dict):
        """
        Inserts a dictionary of {column_name: row_value} into a given table.
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = list(data.values())

        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
        except Error as e:
            print(f"[DB ERROR] Insert failed: {e}")
            print(f"SQL: {sql}")
            print(f"Values: {values}")

    def create_tables(self):
        """
        Creates the raw TfL tables needed for ingestion.
        Safe to run multiple times.
        """

        line_status_sql = """
        CREATE TABLE IF NOT EXISTS tfl_line_status_raw (
            id INT AUTO_INCREMENT PRIMARY KEY,
            line_id VARCHAR(50),
            status_severity INT,
            status_description VARCHAR(255),
            reason TEXT,
            timestamp DATETIME
        );
        """

        arrivals_sql = """
        CREATE TABLE IF NOT EXISTS tfl_arrivals_raw (
            id INT AUTO_INCREMENT PRIMARY KEY,
            line_id VARCHAR(50),
            station_id VARCHAR(50),
            platform VARCHAR(100),
            expected_arrival DATETIME,
            time_to_station INT,
            current_location VARCHAR(255),
            timestamp DATETIME
        );
        """

        try:
            self.cursor.execute(line_status_sql)
            self.cursor.execute(arrivals_sql)
            self.conn.commit()
            print("[DB] Tables created or already exist")
        except Error as e:
            raise Exception(f"[DB ERROR] Table creation failed: {e}")

    def close(self):
        """"
        Close connection to DB
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Connection closed")