# ✈️ Airnote: Plane Detector & Country Quiz

Airnote is a fun, educational Python app that uses real-time aircraft tracking data to detect planes flying near your location. It then traces the plane’s takeoff location and asks you a question about that country — like its capital city!

## 🚀 Features

- 📍 Detect planes randomly around the world
- ✈️ Identify the nearest aircraft using OpenSky Network's live data
- 🛬 Trace the takeoff coordinates using aircraft velocity history
- 🌍 Find the takeoff country with reverse geocoding
- 🧠 Ask a quiz question about that country (e.g., capital)

## 🧑‍💻 How It Works

1. Run get.py to get the icao24 address of a actual random plane
2. Put it in the 'hex' in aircraft.json.
3. It fetches the details of the plane.
4. Ask you the capital of the origin country.
5. Verifies if your input was correct or not.

## 📦 Requirements

- Python 3.8+
- OpenSky Network account (for API access)
- Free API key access from:
  - [OpenSky Network](https://opensky-network.org/)
  - [RESTCountries API](https://restcountries.com/)
- Packages:
  ```bash
  pip install requests geopy


💡 Use Cases
Aviation education

Geography quizzes

Real-time ADS-B plane spotting

Fun hobby projects with RTL-SDR or dump1090

🛠️ Tech Stack
Python

OpenSky REST API

Nominatim (OpenStreetMap reverse geocoder)

RESTCountries API

⚠️ Disclaimer
This project is for educational and recreational use. OpenSky API has rate limits and may require login for full access. Always respect API usage guidelines.

🙌 Acknowledgments
OpenSky Network

OpenStreetMap / Nominatim

RESTCountries API