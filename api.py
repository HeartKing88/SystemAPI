from flask import Flask, request, jsonify
from pymongo import MongoClient
from config import Config
import secrets

app = Flask(__name__)

# MongoDB
client = MongoClient(Config.MONGO_URL)
db = client["api_bot"]
collection = db["keys"]

@app.route("/")
def home():
    return "✅ API Generator Bot Backend Running!"

# Generate API key endpoint
@app.route("/generate", methods=["GET"])
def generate():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"success": False, "error": "Missing user_id"})

    # Agar already key hai to wahi do
    existing = collection.find_one({"user_id": user_id})
    if existing:
        return jsonify({"success": True, "api_key": existing["api_key"]})

    # Nayi key generate
    api_key = secrets.token_hex(16)
    collection.insert_one({"user_id": user_id, "api_key": api_key})

    return jsonify({"success": True, "api_key": api_key})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
