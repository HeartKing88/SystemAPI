import os
import uuid
import pymongo
from pyrogram import Client, filters

MONGO_URL = os.getenv("MONGO_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# MongoDB setup
mongo = pymongo.MongoClient(MONGO_URL)
db = mongo["apikey_bot"]
users = db["users"]

bot = Client("apikey-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
def start(_, msg):
    msg.reply_text(
        "🎶 Welcome to the Music API Bot!\n\n"
        "Use /apikey to get your API key.\n"
        "Use /plan to view your usage."
    )

@bot.on_message(filters.command("apikey"))
def apikey(_, msg):
    user_id = msg.from_user.id
    user = users.find_one({"user_id": user_id})

    if user:
        key = user["api_key"]
    else:
        key = str(uuid.uuid4())
        users.insert_one({"user_id": user_id, "api_key": key, "usage": 0})

    msg.reply_text(
        f"🔑 Your API Key:\n`{key}`\n\n"
        f"✅ You're already registered and ready to use the API!\n\n"
        f"⚠️ Set API_URL=https://yourdomain.com"
    )

@bot.on_message(filters.command("plan"))
def plan(_, msg):
    user = users.find_one({"user_id": msg.from_user.id})
    if not user:
        msg.reply_text("❌ You don’t have an API key yet. Use /apikey")
        return
    
    msg.reply_text(
        f"📊 API Usage\n\n"
        f"Used: {user.get('usage', 0)} requests\n"
        f"Limit: 1000 requests/day"
    )

bot.run()
