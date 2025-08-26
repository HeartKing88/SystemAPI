from pyrogram import Client, filters
from config import Config
import requests

# Bot Client
bot = Client(
    "api_generator_bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Start command
@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "👋 Welcome! Ye bot tumhe YouTube API key generate karke dega.\n\n"
        "API key banane ke liye use karo:\n"
        "`/getkey`"
    )

# Generate API key command
@bot.on_message(filters.command("getkey"))
async def getkey(_, message):
    user_id = message.from_user.id
    api_url = f"{Config.API_BASE_URL}/generate?user_id={user_id}"

    try:
        response = requests.get(api_url).json()
        if response.get("success"):
            await message.reply_text(
                f"✅ Your API Key:\n`{response['api_key']}`"
            )
        else:
            await message.reply_text("❌ API key generate karne me problem aayi.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")

if __name__ == "__main__":
    bot.run()
