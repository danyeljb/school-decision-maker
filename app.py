from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)
    
def init_db():
    conn = sqlite3.connect("submissions.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS submissions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic TEXT,
                        name TEXT,
                        content TEXT,
                        anonymous BOOLEAN,
                        timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect("submissions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT topic, name, content, anonymous, timestamp FROM submissions ORDER BY topic, timestamp DESC")
    submissions = cursor.fetchall()
    conn.close()

    topics = {}
    for topic, name, content, anonymous, timestamp in submissions:
        if topic not in topics:
            topics[topic] = []
        topics[topic].append({"name": name, "content": content, "anonymous": anonymous, "timestamp": timestamp})

    return render_template("index.html", topics=topics)

@app.route('/submit', methods=["POST"])
def submit():
    topic = request.form["topic"].strip()
    name = request.form["name"].strip()
    content = request.form["content"].strip()
    anonymous = request.form.get("anonymous") == "on"

    if anonymous or not name:
        name = "Anonymous"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if topic and content:
        conn = sqlite3.connect("submissions.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO submissions (topic, name, content, anonymous, timestamp) VALUES (?, ?, ?, ?, ?)",
                       (topic, name, content, anonymous, timestamp))
        conn.commit()
        conn.close()

    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Default to 5001 if no PORT is set
    app.run(host="0.0.0.0", port=port)
