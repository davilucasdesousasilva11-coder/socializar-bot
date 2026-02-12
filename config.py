import os
from dotenv import dotenv_values
import discord

env = dotenv_values(".env")

TOKEN = env.get("TOKEN")

PREFIX = "!"

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True

BOT_NAME = "socializar."
BOT_VERSION = "1.0.0"

EMBED_COLOR = 0x2b2d31

SARCASM_LEVEL = 0.3