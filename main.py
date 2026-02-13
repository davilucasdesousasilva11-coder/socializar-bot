import discord
from discord.ext import commands
import os
import asyncio
import sqlite3
from datetime import datetime
import traceback
import random

import config

bot = commands.Bot(

    command_prefix=config.PREFIX, intents=config.INTENTS
)

ultimo_usuario_que_mencionou = None

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
        activity=discord.Activity(
            type=discord.ActivityType.listening, 
            name="Sons da minha guitarra. 🎸"
        )
    )

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if len(message.content) > 5 and random.random() < 0.08:
        try:
            await message.add_reaction("🎸")
        except:
            pass
    
    conteudo = message.content.lower()

    if (
        "quem" in conteudo and "criadora" in conteudo
        and "socializar" in conteudo
    ):
        async with message.channel.typing():
            await asyncio.sleep(1.5)

        if message.author.id == config.OWNER_ID:
            await message.channel.send(f"{message.author.mention} Você, senhorita Kio. 👑")
        else:
            await message.channel.send(f'{message.author.mention} Minha criadora se chama "Kioyichi". 👑')
            return

    if message.content.strip()in (

        f"<@{bot.user.id}>",
        f"<@!{bot.user.id}"
    ):
        async with message.channel.typing():
            await asyncio.sleep(1)
        await message.channel.send(
            f"👋 Olá, {message.author.mention}! Eu sou **{bot.user.name}**\n"
            f"Ainda estou em desenvolvimento 🚧\n"
            f"Em breve terei comandos e funcionalidades novas!"
        )

        global ultimo_usuario_que_mencionou

        if bot.user in message.mentions:

            if ultimo_usuario_que_mencionou == message.author.id:
                await message.channel.send(f"Já estou aqui, {message.author.mention}! 😄")
            else:
                await message.channel.send(f"Oi, {message.author.mention}! Precisa de algo? 😊")

                ultimo_usuario_que_mencionou = message.author.id
                return

        await bot.process_commands(message)


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    print("Iniciando bot...")

if __name__ == "__main__":
    TOKEN = os.environ["TOKEN"]

asyncio.run(main())

bot.run(TOKEN)

    