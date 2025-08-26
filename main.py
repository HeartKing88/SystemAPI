import os
import pymongo
from flask import Flask, request, jsonify

MONGO_URL = os.getenv("MONGO_URL")
mongo = pymongo.MongoClient(MONGO_URL)
db = mongo["apikey_bot"]
users = db["users"]

app = Flask(__name__)

@app.route("/api/download", methods=["GET"])
def download():
    apikey = request.args.get("apikey")
    url = request.args.get("url")

    if not apikey or not url:
        return jsonify({"error": "Missing parameters"}), 400

    user = users.find_one({"api_key": apikey})
    if not user:
        return jsonify({"error": "Invalid API key"}), 403

    # Increase usage
    users.update_one({"api_key": apikey}, {"$inc": {"usage": 1}})

    # Dummy response (yaha YouTube/Spotify download logic aayega)
    return jsonify({
        "status": "success",
        "download_url": f"https://fake-downloader.com/get/{url}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
