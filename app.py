from flask import Flask, request, jsonify
from pymongo import MongoClient
from pytube import Search, YouTube
import random, string, datetime

app = Flask(__name__)

MONGO_URL = "your_mongo_url"
client = MongoClient(MONGO_URL)
db = client["music_api"]
users = db["users"]

def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

@app.route("/generate", methods=["GET"])
def generate():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"success": False, "error": "User ID required"})

    existing = users.find_one({"user_id": user_id})
    if existing:
        return jsonify({"success": True, "api_key": existing["api_key"], "limit": existing["limit"], "expiry": existing["expiry"]})

    key = generate_key()
    expiry = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat()
    users.insert_one({
        "user_id": user_id,
        "api_key": key,
        "plan": "Free",
        "limit": 300,
        "used": 0,
        "expiry": expiry
    })
    return jsonify({"success": True, "api_key": key, "limit": 300, "expiry": expiry})

@app.route("/song", methods=["GET"])
def song():
    query = request.args.get("query")
    apikey = request.args.get("apikey")

    user = users.find_one({"api_key": apikey})
    if not user:
        return jsonify({"success": False, "error": "Invalid API Key"})
    if user["used"] >= user["limit"]:
        return jsonify({"success": False, "error": "Daily limit exceeded"})

    try:
        search = Search(query)
        video = search.results[0]
        yt = YouTube(video.watch_url)
        stream = yt.streams.filter(only_audio=True).first()

        users.update_one({"api_key": apikey}, {"$inc": {"used": 1}})

        return jsonify({
            "success": True,
            "title": yt.title,
            "url": yt.watch_url,
            "audio_url": stream.url
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
