import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "mysecretkey")