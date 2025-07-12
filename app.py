import tkinter as tk
from tkinter import messagebox
import json
import requests

# ---------------- Load Dummy Data ----------------
def load_dummy_data():
    with open("aircraft.json", "r") as f:
        return json.load(f)

# ---------------- OpenSky API Call ----------------
def get_departure_country(icao24):
    url = f"https://opensky-network.org/api/states/all"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for state in data.get("states", []):
                if state[0].lower() == icao24.lower():
                    return state[2]  # origin_country
        return None
    except Exception as e:
        print(f"API error: {e}")
        return None

# ---------------- Get Capital ----------------
def get_capital(country):
    url = f"https://restcountries.com/v3.1/name/{country}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            country_data = response.json()
            return country_data[0]["capital"][0]
    except:
        pass
    return "Unknown"

# ---------------- Ask Question ----------------
def ask_capital_question():
    planes = load_dummy_data()
    if not planes:
        messagebox.showerror("Error", "No dummy data found.")
        return

    plane = planes[0]
    icao24 = plane["hex"]
    origin_country = get_departure_country(icao24)
    
    if not origin_country:
        messagebox.showinfo("Info", "Unable to determine origin country.")
        return

    capital = get_capital(origin_country)

    def check_answer():
        user_answer = answer_entry.get().strip().lower()
        if user_answer == capital.lower():
            messagebox.showinfo("Correct", f"✅ Correct! Capital of {origin_country} is {capital}")
        else:
            messagebox.showerror("Wrong", f"❌ Wrong! Correct answer is {capital}")

    question_label.config(text=f"What is the capital of {origin_country}?")
    answer_entry.delete(0, tk.END)
    submit_button.config(command=check_answer)

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Plane Departure Capital Quiz")

question_label = tk.Label(root, text="Press the button to start", font=("Arial", 14))
question_label.pack(pady=10)

answer_entry = tk.Entry(root, font=("Arial", 12))
answer_entry.pack(pady=5)

submit_button = tk.Button(root, text="Submit Answer", font=("Arial", 12))
submit_button.pack(pady=5)

next_button = tk.Button(root, text="Detect Plane & Ask", font=("Arial", 12), command=ask_capital_question)
next_button.pack(pady=10)

root.mainloop()
