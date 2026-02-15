import discord
from discord.ext import commands
import os
import asyncio
import sqlite3
from datetime import datetime, date
import traceback
import random
import unicodedata
import time

import config

def humor_do_dia():
    hoje = date.today()

    random.seed(hoje.toordinal())
    return random.choice(HUMORES)

bot = commands.Bot(

    command_prefix=config.PREFIX, intents=config.INTENTS
)

ultimo_usuario_que_mencionou = None

HUMORES = [
    "motivado",
    "neutro",
    "cansado",
    "revoltado",
    "triste"
]

CHANCES = {
    "motivado": 0.50,
    "neutro": 0.35,
    "cansado": 0.20,
    "revoltado": 0.15,
    "triste": 0.10
}

estado_bot = {
    "energia": 100,
    "ultimo_regenerar": time.time()
}

def regenerar_energia():
    agora = time.time()
    tempo_passado = agora - estado_bot["ultimo_regenerar"]

    if tempo_passado >= 300:

        estado_bot["energia"] = min(100, estado_bot["energia"] + 2)
        
        estado_bot["ultimo_regenerar"] = agora

@bot.event
async def on_ready():
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    from database import database
    humor = humor_do_dia()

    database.setup()
    
    print("=" * 40)
    print(f"[{agora}] 🤖 Bot conectado como: {bot.user}")
    print(f"🆔 ID: {bot.user.id}")
    print(f"🌐 Servidores: {len(bot.guilds)}")
    print("🚀 Sistema inicializado com sucesso.")
    print(f"🎭 Humor do dia: {humor}")
    print("=" * 40)

    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(e)

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, 
            name="Reclamações da patroa. 🍔"
        )
    )

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    regenerar_energia()

    tempo_digitando = 1.5 if estado_bot["energia"] >= 20 else 3

    conteudo = message.content.lower().strip()

    if conteudo.startswith("oi") and bot.user in message.mentions:
            
            async with message.channel.typing():
                await asyncio.sleep(tempo_digitando)

                if message.author.id == config.OWNER_ID:
                    await message.channel.send(

                        f"{message.author.mention} B-bom dia, senhorita Kio! Eu não tava dormindo no serviço não, juro :3"
                    )
                    return

                else:
                    await message.channel.send(

                        f"{message.author.mention} Bom dia! Em que posso te ajudar hoje? :3"
                    )

                    estado_bot["energia"] -= 5
                    estado_bot["energia"] = max(0, estado_bot["energia"])
                    return

            await bot.process_commands(message)
                            
    if message.author.bot:
        return
    
    if message.author.id == config.YUME_ID and bot.user in message.mentions:
        conteudo = message.content.lower()
        conteudo = remover_acentos(conteudo)

        if "e o salario" in conteudo:
            async with message.channel.typing():
                await asyncio.sleep(tempo_digitando)
                await message.reply(
                    "O salário tá atrasado, Yume. 😔"
                )


    conteudo = message.content.lower()

    if (
        "quem" in conteudo and "criadora" in conteudo
        and "socializar" in conteudo
    ):
        async with message.channel.typing():
            await asyncio.sleep(tempo_digitando)

        if message.author.id == config.OWNER_ID:
            await message.channel.send(f"{message.author.mention} Você, senhorita Kio. 👑")
        else:
            await message.channel.send(f'{message.author.mention} Minha criadora se chama "Kioyichi". 👑')
            return

    if message.content.strip()in (

        f"<@{bot.user.id}>",
        f"<@!{bot.user.id}"
    ):
        if estado_bot["energia"] < 20:
            await asyncio.sleep(2)
        else:
            await asyncio.sleep(1)
        await message.channel.send(
            f"👋 Olá, {message.author.mention}! Eu sou **{bot.user.name}**\n"
            f"Ainda estou em desenvolvimento 🚧\n"
            f"Em breve terei comandos e funcionalidades novas!"
        )

    if bot.user in message.mentions:

        if message.reference:
            try:
                msg_referenciada = await message.channel.fetch_message(

                    message.reference.message_id
                )
                if msg_referenciada.author.id == bot.user.id:
                    return
            except:
                pass

            async with message.channel.typing():
                await asyncio.sleep(1)
                await message.channel.send(
                    f"Oi {message.author.mention}! 👋\nSe precisar de ajuda, é só falar comigo ou com a Kio!"

                )

                return

        await bot.process_commands(message)

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

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

    