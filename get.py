import requests

data = requests.get("https://opensky-network.org/api/states/all").json()
for plane in data["states"][:10]:
    print("ICAO24:", plane[0], "| Country:", plane[2])