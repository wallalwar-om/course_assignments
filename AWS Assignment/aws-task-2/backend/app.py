from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URL = os.getenv("MONGO_URL")
print("MONGO_URL LOADED:", bool(MONGO_URL))

try:
    client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("Connected to MongoDB Atlas!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")

db = client["user_database"]
users_collection = db["users"]

@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()
        print("Received data:", data)

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        if not all(k in data for k in ["name", "age", "city"]):
            return jsonify({"error": "Missing required fields"}), 400

        result = users_collection.insert_one({
            "name": data["name"],
            "age": int(data["age"]),
            "city": data["city"]
        })

        print("Inserted document ID:", str(result.inserted_id))
        return jsonify({"message": "Data submitted successfully"}), 200

    except Exception as e:
        print(f"ERROR in /submit: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Flask is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)