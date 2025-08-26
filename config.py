import os

class Config:
    # Telegram API (my.telegram.org se lo)
    API_ID = int(os.getenv("API_ID", "123456"))
    API_HASH = os.getenv("API_HASH", "your_api_hash")

    # Bot token (@BotFather se lo)
    BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

    # MongoDB connection string (MongoDB Atlas recommended)
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

    # Optional (customizations)
    BOT_OWNER_ID = int(os.getenv("BOT_OWNER
