from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "leaderboard.json")

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


def load_scores():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_scores(scores):
    with open(DATA_FILE, "w") as f:
        json.dump(scores, f, indent=4)


@app.route("/")
def home():
    return "Bomberman Apocalypse Leaderboard Online"


@app.route("/submit", methods=["POST"])
def submit_score():
    data = request.json
    name = data.get("name", "Player")
    score = data.get("score", 0)

    scores = load_scores()
    scores.append({"name": name, "score": score})

    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:20]

    save_scores(scores)

    return jsonify({"status": "success"})


@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    return jsonify(load_scores())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)