from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load data from JSON file
DATA_PATH = os.path.join(os.path.dirname(__file__), "indonesia_national_heroes.json")
with open(DATA_PATH, "r", encoding="utf-8") as file:
    heroes = json.load(file)

@app.route("/")
def home():
    return render_template("index.html", heroes=heroes)

@app.route("/heroes", methods=["GET"])
def get_heroes():
    return jsonify(heroes)

@app.route("/hero/<name>", methods=["GET"])
def get_hero_by_name(name):
    hero = next((h for h in heroes if h["name"].lower() == name.lower()), None)
    if hero:
        return render_template("hero.html", hero=hero)
    return render_template("404.html"), 404

@app.route("/search", methods=["GET"])
def search_heroes():
    query = request.args.get("query", "").lower()
    results = [h for h in heroes if query in h["name"].lower() or query in h["description"].lower()]
    return render_template("search.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)