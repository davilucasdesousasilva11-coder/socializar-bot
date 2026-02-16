import discord
from discord.ext import commands, tasks
import os
import asyncio
import sqlite3
from datetime import datetime, date
import traceback
import random
import unicodedata
import time

import config

memoria_usuarios = {}

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

    atualizar_status.start()

@tasks.loop(minutes=5)
async def atualizar_status():

    humor = humor_do_dia()

    emojis = {
        "motivado": "🔥",
        "neutro": "😐",
        "cansado": "😴",
        "revoltado": "😡",
        "triste": "🌧️"
    }

    emoji = emojis.get(humor, "😐")

    await bot.change_presence(

    activity=discord.CustomActivity(
        name=f"{emoji} Humor atual: {humor}"
    )
)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    regenerar_energia()
    
    user_id = message.author.id

    if user_id not in memoria_usuarios:
        memoria_usuarios[user_id] = {

            "mensagens": 0,
            "ultima_interacao": None,
            "usou_oi": False
        }

        memoria_usuarios[user_id]["mensagens"] += 1
        memoria_usuarios[user_id]["ultima_interacao"] = time.time()

    tempo_digitando = 1.5 if estado_bot["energia"] >= 20 else 3

    conteudo = message.content.lower().strip()

    if conteudo.startswith("oi") and bot.user in message.mentions:
            
            async with message.channel.typing():
                await asyncio.sleep(tempo_digitando)

                if message.author.id == config.OWNER_ID:

                    memoria_usuarios[user_id]["usou_oi"] = True


                    await message.channel.send(

                        f"{message.author.mention} B-bom dia, senhorita Kio! Eu não tava dormindo no serviço não, juro :3"
                    )
                    estado_bot["energia"] -= 5
                    estado_bot["energia"] = max(0, estado_bot["energia"])
                    return

                else:

                    memoria_usuarios[user_id]["usou_oi"] = True

                    await message.channel.send(

                        f"{message.author.mention} Bom dia! Em que posso te ajudar hoje? :3"
                    )

                    estado_bot["energia"] -= 5
                    estado_bot["energia"] = max(0, estado_bot["energia"])
                    return

            await bot.process_commands(message)
    
    if message.author.id == config.YUME_ID and bot.user in message.mentions:
        conteudo = message.content.lower()
        conteudo = remover_acentos(conteudo)

        if "e o salario" in conteudo:
            async with message.channel.typing():
                await asyncio.sleep(tempo_digitando)
                await message.reply(
                    "O salário tá atrasado, Yume. 😔"
                )

                estado_bot["energia"] -= 3
                estado_bot["energia"] = max(0, estado_bot["energia"])

                return


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

    if message.content.strip() in (
        f"<@bot.user.id>",
        f"<@${bot.user.id}>"
    ):
        tempo_digitando = 1.2 if estado_bot["energia"] >= 20 else 2.5

        async with message.channel.typing():
            await asyncio.sleep(tempo_digitando)

            if message.author.id == config.OWNER_ID:

                resposta = (
                    f"👑 {message.author.mention} Oi, senhorita Kio! Eu tô aqui pra te ajudar no que precisar :3"
                )
            else:
                resposta = (
            f"🫂 Olá, {message.author.mention}! Eu sou **{bot.user.name}**\n"
            f"🔨 Atualmente, ainda estou em **desenvolvimento**\n"
            f"👑 Fale com minha criadora **Kioyichi** caso tenha alguma dúvida!"
        )
                await message.channel.send(resposta)

                estado_bot["energia"] -= 4
                estado_bot["energia"] = max(0, estado_bot["energia"])
                return
            
    if message.reference and message.reference.resolved:
        if message.reference.resolved.author == bot.user:

            async with message.channel.typing():
                await asyncio.sleep(tempo_digitando)

                await message.channel.send(
                    f"{message.author.mention} Posso te ajudar em algo? :3"
                )

                estado_bot["energia"] -= 4
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

    