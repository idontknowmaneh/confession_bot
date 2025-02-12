from flask import Flask, jsonify, render_template, request, redirect, url_for
import threading
import sqlite3
import random
import string
from bot import run_bot  # Import the bot run function

app = Flask(__name__)
app.config.from_object('config')

# Helper function to generate a random 10-character string
def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Helper function to insert confession data into the SQLite database
def insert_confession(unique_id, message, file_path=None):
    conn = sqlite3.connect('confessions.db')
    c = conn.cursor()
    
    # Create the table if it does not exist (id is the primary key)
    c.execute('''CREATE TABLE IF NOT EXISTS confessions (
                    id TEXT PRIMARY KEY,
                    message TEXT,
                    file_path TEXT)''')
    
    # Insert the confession data into the database
    c.execute("INSERT INTO confessions (id, message, file_path) VALUES (?, ?, ?)",
              (unique_id, message, file_path))
    
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Capture form data
        message = request.form["message"]
        
        # Capture the uploaded file if any
        uploaded_file = request.files["upload"]
        file_path = None
        if uploaded_file:
            file_path = f"uploads/{uploaded_file.filename}"
            uploaded_file.save(file_path)

        # Generate a random unique ID for this confession
        unique_id = generate_unique_id()

        # Insert the confession data into the database
        insert_confession(unique_id, message, file_path)

        # Redirect the user to the confirmation page
        return redirect(url_for('confirmation', unique_id=unique_id))

    return render_template("dark.html")

@app.route("/confirmation/<unique_id>")
def confirmation(unique_id):
    return render_template("confirmation.html", unique_id=unique_id)

def run_flask():
    # Run Flask in the main thread
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)  # Disable reloader to avoid issues

if __name__ == "__main__":
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Run Flask in the main thread
    run_flask()
