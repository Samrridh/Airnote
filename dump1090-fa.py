# --- Configuration for dump1090-fa ---
DUMP1090_HOST = "127.0.0.1"
DUMP1090_PORT = 8080 

# ---------------- API Functions ----------------

def get_random_plane_data():
    """Fetches data for a random plane from dump1090-fa."""
    url = f"http://{DUMP1090_HOST}:{DUMP1090_PORT}/data/aircraft.json"
    try:
        response = requests.get(url, timeout=5) 
        response.raise_for_status()
        data = response.json()
        aircraft = data.get("aircraft", [])

        if not aircraft:
            print("No aircraft found from dump1090-fa API.")
            return None, None

        valid_aircraft = [a for a in aircraft if a.get("hex")]

        if not valid_aircraft:
            print("No valid aircraft with ICAO24 found from dump1090-fa.")
            return None, None

        random_plane = random.choice(valid_aircraft)
        icao24 = random_plane["hex"]
        
        origin_country = None 

        return origin_country, icao24

    except requests.exceptions.RequestException as e:
        print(f"Error fetching plane data from dump1090-fa: {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from dump1090-fa API: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred in get_random_plane_data (dump1090-fa): {e}")
        return None, None