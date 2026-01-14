import datetime
import requests

# Replace with your actual API key from National Rail
API_KEY = "YOUR_API_KEY_HERE"

STATION_CODE = "LST"

def fetch_departures(station_code: str):
    url = f"https://api1.raildata.org.uk/ldb/v1/departures/{station_code}"
    headers = {
        "x-apikey": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"API error: {response.status_code} - {response.text}")

    return response.json()

def main():
    print(f"Fetching live departures for {STATION_CODE} at {datetime.datetime.now()}")
    data = fetch_departures(STATION_CODE)

    # Print a few key fields
    for service in data.get("trainServices", []):
        std = service.get("std")  # scheduled departure
        etd = service.get("etd")  # estimated departure
        dest = service.get("destination", [{}])[0].get("locationName")

        print(f"{std} → {dest} | Expected: {etd}")

if __name__ == "__main__":
    main()