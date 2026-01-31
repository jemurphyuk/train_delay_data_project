from fetch_departures import TflIngestion
from storage import RawDatabase
from config import Config

def main():
    print("Starting ingestion ...")
    db = RawDatabase()
    print("Creating tables ...")
    db.create_tables()
    ingestor = TflIngestion()
    ingestor.ingest_all(Config.DEFAULT_LINE)
    db.close()
    print("Ingestion completed")

if __name__ == "__main__":
    main()