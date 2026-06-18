from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "leaderboard.db")


# ✅ Initialize database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return "Bomberman Apocalypse Leaderboard Online (SQLite)"


@app.route("/submit", methods=["POST"])
def submit_score():

    data = request.json
    name = data.get("name", "Player")
    score = int(data.get("score", 0))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scores (name, score) VALUES (?, ?)",
        (name, score)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})


@app.route("/leaderboard", methods=["GET"])
def leaderboard():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, score FROM scores ORDER BY score DESC LIMIT 20"
    )

    rows = cursor.fetchall()
    conn.close()

    results = [{"name": row[0], "score": row[1]} for row in rows]

    return jsonify(results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
