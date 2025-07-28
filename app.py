from flask import Flask, render_template, request, session, redirect, url_for
import json
import requests
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'easteregg')

# ---------------- Dump1090 data ----------------
DUMP1090_HOST = "62.45.168.247"
DUMP1090_PORT = 7878

def get_random_icao24():
    url = f"http://{DUMP1090_HOST}:{DUMP1090_PORT}/data/aircraft.json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        aircraft = data.get("aircraft", [])
        valid_aircraft = [a for a in aircraft if a.get("hex")]

        if not valid_aircraft:
            print("No valid aircraft with ICAO24 found from dump1090-fa.")
            return None

        random_plane = random.choice(valid_aircraft)
        icao24 = random_plane["hex"]
        return icao24

    except Exception as e:
        print(f"Unexpected error in get_random_icao24: {e}")
        return None

def get_origin_country_from_opensky(icao24):
    url = "https://opensky-network.org/api/states/all"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        states = response.json().get("states", [])

        for state in states:
            if state[0].lower() == icao24.lower():
                country = state[2]
                return country  

        return None  
    except requests.RequestException as e:
        print("Error querying OpenSky API:", e)
        return None

# ---------------- Opensky data ----------------

def get_random_plane_data():
    url = "https://opensky-network.org/api/states/all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  
        data = response.json()
        states = data.get("states", [])

        if not states:
            print("No states found from OpenSky Network API.")
            return None, None 

        valid_states = [s for s in states if s and len(s) > 2 and s[2] and s[0]]
        if not valid_states:
            print("No valid states with country information found.")
            return None, None


        random_plane = random.choice(valid_states)
        icao24 = random_plane[0]  
        origin_country = random_plane[2] 

        return origin_country, icao24

    except requests.exceptions.RequestException as e:
        print(f"Error fetching plane data: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred in get_random_plane_data: {e}")
        return None, None


# Common for both cases 
def get_capital(country):
    if not country:
        return "Unknown"
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country}", timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list) and data[0].get("capital"):
            return data[0]["capital"][0] 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching capital for {country}: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from RestCountries API for {country}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in get_capital for {country}: {e}")
    return "Unknown"
    
@app.route("/", methods=["GET", "POST"])
def index():
    # Handle mode switching
    mode = request.args.get("mode")
    if mode in ["opensky", "dump1090"]:
        session["mode"] = mode
    elif "mode" not in session:
        session["mode"] = "opensky"  # default

    selected_mode = session["mode"]

    if request.method == "POST":
        user_answer = request.form.get("answer", "").strip().lower()
        correct_capital = session.get("capital", "").strip().lower()

        if user_answer == correct_capital and correct_capital != "unknown":
            session["result"] = "✅ Correct!"
        elif correct_capital == "unknown":
            session["result"] = "❌ Could not determine the correct capital for this country."
        else:
            session["result"] = f"❌ Wrong! The correct answer was {session.get('capital')}"

        country_to_guess = session.get("origin_country")
        return render_template("index.html", country=country_to_guess, result=session["result"], mode=selected_mode)

    # New game logic
    if "capital" not in session or session.get("result") is not None:
        session["result"] = None

        if selected_mode == "dump1090":
            icao24 = get_random_icao24()
            origin_country = get_origin_country_from_opensky(icao24) if icao24 else None
        else:  # opensky
            origin_country, icao24 = get_random_plane_data()

        capital = get_capital(origin_country)
        session["origin_country"] = origin_country or "a country"
        session["capital"] = capital or "Unknown"

        if not origin_country or capital == "Unknown":
            session["result"] = "Could not fetch a valid question. Please try again."

    country_to_guess = session.get("origin_country")
    result_message = session.get("result")
    return render_template("index.html", country=country_to_guess, result=result_message, mode=selected_mode)


@app.route("/new_game")
def new_game():
    session.pop("origin_country", None)
    session.pop("capital", None)
    session.pop("result", None)
    return redirect(url_for('index', mode=session.get("mode", "opensky")))

if __name__ == "__main__":
    app.run(debug=True)