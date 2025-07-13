from flask import Flask, render_template, request, session, redirect, url_for
import json
import requests
import random
import os

app = Flask(__name__)
# for testing only
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'easteregg')

# ---------------- API Functions ----------------

def get_random_plane_data():
    """Fetches data for a random plane from OpenSky Network."""
    url = "https://opensky-network.org/api/states/all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  
        data = response.json()
        states = data.get("states", [])

        if not states:
            print("No states found from OpenSky Network API.")
            return None, None 

        # Filter out states without a country or invalid icao24
        valid_states = [s for s in states if s and len(s) > 2 and s[2] and s[0]]
        if not valid_states:
            print("No valid states with country information found.")
            return None, None

        # Select a random plane from the valid states
        random_plane = random.choice(valid_states)
        icao24 = random_plane[0]  
        origin_country = random_plane[2] 

        return origin_country, icao24

    except requests.exceptions.RequestException as e:
        print(f"Error fetching plane data: {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from OpenSky API: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred in get_random_plane_data: {e}")
        return None, None

def get_capital(country):
    """Fetches the capital city for a given country."""
    if not country:
        return "Unknown"
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country}", timeout=10)
        response.raise_for_status()
        data = response.json()
        # The API returns a list of countries, take the first one
        if data and isinstance(data, list) and data[0].get("capital"):
            return data[0]["capital"][0] # Capital is usually a list, take the first
    except requests.exceptions.RequestException as e:
        print(f"Error fetching capital for {country}: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from RestCountries API for {country}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred in get_capital for {country}: {e}")
    return "Unknown"

# ---------------- Flask Routes ----------------

@app.route("/", methods=["GET", "POST"])
def index():
    result_message = session.get("result") 

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
        return render_template("index.html", country=country_to_guess, result=session["result"])

    if "capital" not in session or session.get("result") is not None:
        session["result"] = None

        origin_country, icao24 = get_random_plane_data()
        capital = get_capital(origin_country)


        session["origin_country"] = origin_country
        session["capital"] = capital


        if not origin_country or capital == "Unknown":
            session["origin_country"] = "a country" # pookie
            session["capital"] = "Unknown"
            session["result"] = "Could not fetch a valid question. Please try again."
    
    country_to_guess = session.get("origin_country")
    result_message = session.get("result") 

    return render_template("index.html", country=country_to_guess, result=result_message)

@app.route("/new_game")
def new_game():
    """Resets the game by clearing the session and redirecting to the index.
    This effectively acts as the 'Refresh' button."""
    session.pop("origin_country", None)
    session.pop("capital", None)
    session.pop("result", None) 
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)