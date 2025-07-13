# from flask import Flask, render_template, request
# import json, requests

# app = Flask(__name__)


# # ---------------- Write Dummy Data (integrating get.py) ----------------
# def write_real_data():
#     data = requests.get("https://opensky-network.org/api/states/all").json()
#     for plane in data["states"][:2]:
#         data = [
#             {
#                 "hex": plane[0],
#                 "flight": plane[1],
#                 "altitude": plane[13],
#                 "country":plane[2],
#                 "lat": plane[6],
#                 "lon": plane[5]
#             }
#         ]
#     with open("aircraft.json", "w") as f:
#         json.dump(data, f, indent=4)


# # ---------------- Dummy Data ----------------
# def load_dummy_data():
#     with open("aircraft.json", "r") as f:
#         return json.load(f)

# # ---------------- API ----------------
# def get_departure_country(icao24, steps):
#     url = f"https://opensky-network.org/api/states/all"
#     steps.append("🛰️ Fetching real-time aircraft data...")
#     try:
#         response = requests.get(url, timeout=10)
#         if response.status_code == 200:
#             data = response.json()
#             for state in data.get("states", []):
#                 if state[0].lower() == icao24.lower():
#                     steps.append(f"🌍 Found origin country: {state[2]}")
#                     return state[2]
#         steps.append("⚠️ Could not find origin country.")
#         return None
#     except:
#         steps.append("❌ Failed to fetch origin country.")
#         return None

# def get_capital(country, steps):
#     steps.append(f"🏙️ Finding capital of {country}...")
#     try:
#         response = requests.get(f"https://restcountries.com/v3.1/name/{country}", timeout=10)
#         if response.status_code == 200:
#             capital = response.json()[0]["capital"][0]
#             steps.append(f"✅ Capital found: {capital}")
#             return capital
#     except:
#         pass
#     steps.append("❌ Could not find capital.")
#     return "Unknown"

# @app.route("/", methods=["GET", "POST"])
# def index():
#     steps = []
#     steps.append("✈️ Loading dummy aircraft data...")
#     write_real_data()
#     plane = load_dummy_data()[0]
#     icao24 = plane["hex"]
#     steps.append(f"🔎 Found aircraft: HEX={icao24}")

#     origin_country = get_departure_country(icao24, steps)
#     capital = get_capital(origin_country, steps) if origin_country else "Unknown"

#     result = None
#     if request.method == "POST":
#         answer = request.form.get("answer", "").strip().lower()   
#         correct = capital.lower()
#         if answer == correct:
#             result = "✅ Correct!"
#         else:
#             result = f"❌ Wrong! Correct answer is {capital}"

#     return render_template("index.html", country=origin_country, result=result, steps=steps)

# if __name__ == "__main__":
#     app.run(debug=True)




from flask import Flask, render_template, request, Response, stream_with_context
import json, requests, random, time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start_quiz():
    @stream_with_context
    def generate():
        yield "data: ✈️ Loading dummy aircraft data...\n\n"
        time.sleep(1)

        data = requests.get("https://opensky-network.org/api/states/all").json()
        planes = data["states"]
        valid_planes = [p for p in planes if p[0] and p[2] and p[5] and p[6]]

        if not valid_planes:
            yield "data: ❌ No valid planes found.\n\n"
            return

        plane = random.choice(valid_planes)
        icao24 = plane[0]
        yield f"data: 🔎 Found aircraft: HEX={icao24}\n\n"
        time.sleep(1)

        origin_country = plane[2]
        yield f"data: 🌍 Found origin country: {origin_country}\n\n"
        time.sleep(1)

        capital = get_capital(origin_country)
        yield f"data: ✅ Capital found: {capital}\n\n"
        yield f"data: END|{origin_country}|{capital}\n\n"  # signal end of stream

    return Response(generate(), mimetype='text/event-stream')

def get_capital(country):
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country}", timeout=10)
        if response.status_code == 200:
            return response.json()[0]["capital"][0]
    except:
        pass
    return "Unknown"

if __name__ == "__main__":
    app.run(debug=True)
