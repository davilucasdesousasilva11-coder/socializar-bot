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
import json

import config

memoria_usuarios = {}

def carregar_estado():
    global humor_atual, nivel_emocional, ultimo_dia

    try:
        with open(EMOTION_FILE, "r") as f:
            dados = json.load(f)
            humor_atual = dados["humor"]
            nivel_emocional = dados["nível"]
            ultimo_dia = dados["dia"]
    except:
        humor_atual = "neutro"
        nivel_emocional = 0
        ultimo_dia = None

def salvar_estado():
    with open(EMOTION_FILE, "w") as f:

        json.dump({
            "humor": humor_atual,
            "nivel": nivel_emocional,
            "dia": ultimo_dia
        }, f)

def atualizar_humor_diario():
    global humor_atual, ultimo_dia

    hoje = str(datetime.date.today())

    if ultimo_dia != hoje:
        ultimo_dia = hoje

        if humor_atual == "feliz":
            humor_atual = random.choices(

                ["feliz", "neutro", "irritado"],
                weights=[50, 30, 20]
            )[0]

        elif humor_atual == "irritado":
            humor_atual = random.choices(
                ["irritado", "neutro", "feliz"],
                weights=[50, 30, 20]
            )[0]

        else:
            humor_atual = random.choice(["feliz", "neutro", "irritado"])
                                         
            salvar_estado()


bot = commands.Bot(

    command_prefix=config.PREFIX, intents=config.INTENTS
)

ultimo_usuario_que_mencionou = None

EMOTION_FILE = "emotion_state.json"

humor_atual = "neutro"
nivel_emocional = 0
ultimo_dia = None


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

status_index = 0

@tasks.loop(seconds=5)
async def atualizar_status():
    global status_index
    
    servidores = len(bot.guilds)
    usuarios = sum(g.members_count for g in bot.guilds)

    lista_status = [
        f"🎭 Humor:{humor_atual}",
        f"🌡️ Nível Emocional: {nivel_emocional}",
        f"👀 Observando {usuarios} humanos...",
        f"🩷 Online para {servidores} servidores",
        f"🧠 Desenvolvendo autoconsciência...",
        f"😵‍💫 ERRO 404: SALÁRIO NOT FOUND"
    ]

    activity = discord.Activity(
        type=discord.ActivityType.custom,

        name=lista_status[status_index]
    )

    await bot.change_presence(activity=activity)

    status_index = (status_index +1) % len(lista_status)

@bot.event
async def on_ready():
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    from database import database
    carregar_estado()
    atualizar_humor_diario()

    if not atualizar_status.is_running():
        atualizar_status.start()

        print("Custom status iniciado. 🎭")

    database.setup()
    
    print("=" * 40)
    print(f"[{agora}] 🤖 Bot conectado como: {bot.user}")
    print(f"🆔 ID: {bot.user.id}")
    print(f"🌐 Servidores: {len(bot.guilds)}")
    print("🚀 Sistema inicializado com sucesso.")
    print(f"🎭 Humor atual: {humor_atual}")
    print("=" * 40)

    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(e)




@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    def ajustar_emocao(conteudo):
        global nivel_emocional, humor_atual

        palavras_boas = ["amo", "legal", "bom", "fofo"]
        palavras_ruins = ["chato", "odeio", "burro", "ruim"]

        if any(p in conteudo for p in palavras_boas):
            nivel_emocional += 1
        
        if any(p in conteudo for p in palavras_ruins):
            nivel_emocional -= 1

        if nivel_emocional >= 5:
            humor_atual = "feliz"

        elif nivel_emocional <= -5:
            humor_atual = "irritado"

            salvar_estado()

        
    
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
        f"<@{bot.user.id}>",
        f"<@${bot.user.id}>"
    ):


        if message.author.id == config.OWNER_ID:
                async with message.channel.typing():
                    await asyncio.sleep(tempo_digitando)
                    await message.reply(
                        f"👑 {message.author.mention} Oi, senhorita Kio! Tô aqui caso precise de testes! :3")
                    return
        else:
            async with message.channel.typing():
                await asyncio.sleep(tempo_digitando)
            await message.channel.send(
            f"🫂 Olá, {message.author.mention}! Eu sou **{bot.user.name}**\n"
            f"🔨 Atualmente, ainda estou em **desenvolvimento**\n"
            f"👑 Fale com minha criadora **Kioyichi** caso tenha alguma dúvida!"
        )
            

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

    conteudo = message.content.lower()


    if (
        message.author.id == config.YUME_ID and bot.user in message.mentions and any(conteudo.startswith(frase) for frase in ["eu te amo", "te amo"])
    ):
        async with message.channel.typing():
            await asyncio.sleep(tempo_digitando)

        await message.reply(
            f"Eu também te amo, {message.author.mention} :3 💖"
        )

        estado_bot["energia"] -= 3
        estado_bot["energia"] = max(0, estado_bot["energia"])
        return
    
    conteudo = message.content.lower().strip()

    if conteudo in ["tendi", "tendeu", "entendi"]:
        async with message.channel.typing():
            await asyncio.sleep(tempo_digitando)
            await message.reply("eu também tendi :P")
            return

        estado_bot["energia"] -= 2
        estado_bot["energia"] = max(0, estado_bot["energia"])
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

    