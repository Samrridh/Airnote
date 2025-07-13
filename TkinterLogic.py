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
