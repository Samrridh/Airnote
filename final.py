import requests
import time
import csv

# Step 1: Get aircraft from dump1090 web interface
def get_aircraft_from_dump1090():
    try:
        r = requests.get("http://localhost:8080/data.json", timeout=3)
        aircraft = r.json()
        if not aircraft:
            print("❌ No aircraft detected.")
            return None
        print(f"✈️ Found {len(aircraft)} aircraft. Taking first.")
        return aircraft[0]  # Take first one
    except Exception as e:
        print("Error getting data from dump1090:", e)
        return None

# Step 2: Get departure airport from OpenSky API
def get_departure_airport(icao24):
    now = int(time.time())
    begin = now - 6 * 3600  # 6 hours ago
    url = "https://opensky-network.org/api/flights/aircraft"
    params = {
        "icao24": icao24,
        "begin": begin,
        "end": now
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        flights = r.json()
        if not flights:
            print("❌ No flight data found.")
            return None
        flight = flights[0]
        return flight.get("estDepartureAirport")
    except Exception as e:
        print("Error accessing OpenSky API:", e)
        return None

# Step 3: Map airport to country
def get_country_from_icao(icao_code, csv_file='airports.csv'):
    try:
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['icao'] == icao_code:
                    return row['iso_country']
    except Exception as e:
        print("Error reading airport database:", e)
    return "Unknown"

# Step 4: Optional trivia dictionary
country_trivia = {
    "IN": "What is the capital of India?",
    "US": "What is the capital of the USA?",
    "GB": "What is the capital of the UK?",
    "FR": "What is the capital of France?",
    "AE": "What is the capital of the UAE?",
    "SG": "What is the capital of Singapore?",
}

# Main function
def main():
    aircraft = get_aircraft_from_dump1090()
    if not aircraft:
        return
    icao24 = aircraft['hex']
    flight = aircraft.get('flight', '').strip()
    print(f"➡️ ICAO24: {icao24}, Flight: {flight}")

    departure_icao = get_departure_airport(icao24)
    if not departure_icao:
        return
    print(f"🛫 Departure Airport ICAO: {departure_icao}")

    country_code = get_country_from_icao(departure_icao)
    print(f"🌍 Departure Country: {country_code}")

    if country_code in country_trivia:
        print(f"🎯 Trivia: {country_trivia[country_code]}")
    else:
        print("No trivia available for this country.")

if __name__ == "__main__":
    main()
