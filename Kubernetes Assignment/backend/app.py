from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URL = os.getenv("MONGO_URL")
print("MONGO_URL LOADED:", bool(MONGO_URL))

client = MongoClient(MONGO_URL)
db = client["user_database"]
users_collection = db["users"]

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

    # FORCE crash if Mongo fails
    result = users_collection.insert_one({
        "name": data["name"],
        "age": int(data["age"]),
        "city": data["city"]
    })

    return jsonify({"message": "Data submitted successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
