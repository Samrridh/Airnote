import requests
import time
from datetime import datetime

# Delhi bounding box
lamin = 28.4
lomin = 76.9
lamax = 28.9
lomax = 77.5

print("🔍 Fetching planes flying over Delhi...")

# Step 1: Get current planes overhead
resp = requests.get(
    "https://opensky-network.org/api/states/all",
    params={"lamin": lamin, "lomin": lomin, "lamax": lamax, "lomax": lomax}
)
data = resp.json()
states = data.get("states", [])

if not states:
    print("❌ No aircraft found overhead.")
    exit()

# Take first aircraft
icao24 = states[0][0]
callsign = states[0][1].strip()
origin_country = states[0][2]
print(f"✈️ Aircraft: {callsign}, Country: {origin_country}, ICAO24: {icao24}")

# Step 2: Get flight history (last 6 hours)
now = int(time.time())
begin = now - 6 * 3600

flight_resp = requests.get(
    f"https://opensky-network.org/api/flights/aircraft",
    params={"icao24": icao24, "begin": begin, "end": now}
)
flights = flight_resp.json()

if not flights:
    print("❌ No flight history found.")
    exit()

flight = flights[0]
departure_airport = flight.get("estDepartureAirport", "Unknown")
arrival_airport = flight.get("estArrivalAirport", "Unknown")

print(f"🛫 Departure Airport: {departure_airport}")
print(f"🛬 Arrival Airport: {arrival_airport}")

# Step 3: Map airport code to country (example mapping)
airport_country_map = {
    "VIDP": "India",
    "VABB": "India",
    "OMDB": "UAE",
    "EGLL": "United Kingdom",
    "LFPG": "France",
    "KJFK": "USA"
}

departure_country = airport_country_map.get(departure_airport, "Unknown")

print(f"🌍 Departure Country: {departure_country}")
