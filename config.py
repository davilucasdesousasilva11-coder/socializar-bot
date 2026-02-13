import os
import discord
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")

OWNER_ID = 1330568796511014922

PREFIX = "$"

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True

BOT_NAME = "socializar."
BOT_VERSION = "1.0.0"

EMBED_COLOR = 0x2b2d31

SARCASM_LEVEL = 0.3

YUME_ID = 809826760241053737