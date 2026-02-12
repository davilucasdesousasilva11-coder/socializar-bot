import discord
from discord.ext import commands
import os
import asyncio
import sqlite3
from datetime import datetime

import config

bot = commands.Bot(

    command_prefix=config.PREFIX, intents=config.INTENTS
)

@bot.event
async def on_ready():
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    from database import database

    database.setup()
    
    print("=" * 40)
    print(f"[{agora}] 🤖 Bot conectado como: {bot.user}")
    print(f"🆔 ID: {bot.user.id}")
    print(f"🌐 Servidores: {len(bot.guilds)}")
    print("🚀 Sistema inicializado com sucesso.")
    print("=" * 40)

    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(e)

    await bot.change_presence(
        atividade=discord.Activity(
            type=discord.ActivityType.listening, 
            name="Sons da minha guitarra. 🎸"
        )
    )

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_cogs()
        print("Iniciando bot...")
        await bot.start(config.TOKEN)

asyncio.run(main())

    