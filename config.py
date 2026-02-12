import os
import discord
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")

print("CONFIG TOKEN:", TOKEN)

PREFIX = "!"

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True

BOT_NAME = "socializar."
BOT_VERSION = "1.0.0"

EMBED_COLOR = 0x2b2d31

SARCASM_LEVEL = 0.3