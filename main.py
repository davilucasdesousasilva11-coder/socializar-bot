# ======= IMPORTS =======

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

# ======= CONFIGS. INICIAIS =======

memoria_usuarios = {}

def humor_do_dia():
    hoje = date.today()

    random.seed(hoje.toordinal())
    return random.choice(HUMORES)

bot = commands.Bot(

    command_prefix=config.PREFIX, intents=config.INTENTS
)

ultimo_usuario_que_mencionou = None

# ======= SISTEMA DE HUMORES =======

humor_base = "neutro"
humor_forcado = None



HUMORES = [
    "motivado",
    "neutro",
    "cansado",
    "revoltado",
    "triste",
    "amoroso",
    "feliz"
]

humores_validos = [
    "amoroso",
    "pensativo",
    "desconfiado",
    "assustado",
    "feliz",
    "neutro",
    "irritado",
    "triste",
    "cansado"
]

CHANCES = {
    "motivado": 0.50,
    "neutro": 0.35,
    "cansado": 0.20,
    "revoltado": 0.15,
    "triste": 0.10,
    "amoroso": 0.40,
    "pensativo": 0.25,
    "desconfiado": 0.12,
    "assustado": 0.05,
    "feliz": 0.55
}

# ======= SISTEMA DE ENERGIA =======

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


# ======= EVENTOS =======

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

# ======= STATUS AUTOMÁTICO =======

@tasks.loop(minutes=5)
async def atualizar_status():
    global humor_forcado
    humor_exibido = humor_forcado if humor_forcado else humor_do_dia()

    emojis = {
        "motivado": "🔥",
        "neutro": "😐",
        "cansado": "😴",
        "revoltado": "😤",
        "triste": "😭",
        "amoroso": "😍",
        "pensativo": "🤔",
        "desconfiado": "🤨",
        "assustado": "😱",
        "feliz": "🥳"
    }

    emoji = emojis.get(humor_do_dia, "🎭")

    await bot.change_presence(

    activity=discord.CustomActivity(
        name=f"{emoji} Humor atual: {humor_do_dia()}"
    )
)


# ======= ON MESSAGE =======

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    conteudo_original = message.content
    conteudo = conteudo_original.lower().strip()
    conteudo_sem_acentos = remover_acentos(conteudo)
    
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

    # COMANDO DONO: FORÇAR HUMOR =======

    if message.author.id == config.OWNER_ID and conteudo.startswith("fique "):
            async with message.channel.typing():
                await asyncio.sleep(tempo_digitando)

            try:
                parte = conteudo.replace("fique ", "")
                novo_humor = parte.split(",")[0].strip()

                if novo_humor in humores_validos:
                    humor_forcado = novo_humor

                    await atualizar_status()

                    humor_exibido = humor_forcado if humor_forcado else humor_do_dia

                    emojis = {
        "motivado": "🔥",
        "neutro": "😐",
        "cansado": "😴",
        "revoltado": "😤",
        "triste": "😭",
        "amoroso": "😍",
        "pensativo": "🤔",
        "desconfiado": "🤨",
        "assustado": "😱",
        "feliz": "🥳"
     }
                    emoji = emojis.get(humor_do_dia, "🎭")

                    await bot.change_presence(

                        status=discord.Status.online,

                        activity=discord.CustomActivity(
        name=f"{emoji} Humor atual: {humor_exibido}"
    )
                    )
                    await message.channel.send(f"{message.author.mention} Okay! Agora estou {novo_humor} :3")
                else:
                    await message.channel.send(f"Hmm, esse humor não existe, {message.author.mention} :(")
            except:
                await message.channel.send(f"Formato inválido, {message.author.mention} 😭")
    
    # ======= SAUDAÇÃO =======

    if conteudo.startswith("oi") and bot.user in message.mentions:
            
            async with message.channel.typing():
                await asyncio.sleep(tempo_digitando)

                if message.author.id == config.OWNER_ID:

                    memoria_usuarios[user_id]["usou_oi"] = True


                    await message.channel.send(

                        f"{message.author.mention} Sensei Kio! Hai! Eu estava treinando o meu Star Platinum :3"
                    )
                    estado_bot["energia"] -= 5
                    estado_bot["energia"] = max(0, estado_bot["energia"])
                    return

                else:

                    memoria_usuarios[user_id]["usou_oi"] = True

                    await message.channel.send(

                        f"{message.author.mention} Hai! Como você está, civil? "
                    )

                    estado_bot["energia"] -= 5
                    estado_bot["energia"] = max(0, estado_bot["energia"])
                    return

            await bot.process_commands(message)

            # ======= RESPOSTA DIO =======
    
    if message.author.id == config.YUME_ID and bot.user in message.mentions:
        conteudo = message.content.lower()
        conteudo = remover_acentos(conteudo)

        if "e o dio" in conteudo:
            async with message.channel.typing():
                await asyncio.sleep(tempo_digitando)
                await message.reply(
                    "Ainda macetando o Pocchi...\n"
                    "ou provavelmente procurando corpos alheios por aí."
                )

                estado_bot["energia"] -= 3
                estado_bot["energia"] = max(0, estado_bot["energia"])

                return


    # ======= RESPOSTA CRIADORA =======

    if (
        "quem" in conteudo and "criadora" in conteudo
        and "socializar" in conteudo
    ):
        async with message.channel.typing():
            await asyncio.sleep(tempo_digitando)

        if message.author.id == config.OWNER_ID:
            await message.channel.send(f"{message.author.mention} Você, sensei Kio. 👑")
        else:
            await message.channel.send(f'{message.author.mention} Minha sensei se chama "Kioyichi". 👑')
            return

    if message.content.strip() in (
        f"<@{bot.user.id}>",
        f"<@${bot.user.id}>"
    ):

        # ======= RESPOSTA A MENÇÃO DIRETA =======

        if message.author.id == config.OWNER_ID:
                async with message.channel.typing():
                    await asyncio.sleep(tempo_digitando)
                    await message.reply(
                        f"👑 {message.author.mention} Hai, Kio-sama! Tô aqui caso precise de testes! :3")
                    return
        else:
            async with message.channel.typing():
                await asyncio.sleep(tempo_digitando)
            await message.channel.send(
            f"🫂 Olá, {message.author.mention}! Eu sou **{bot.user.name}**\n"
            f"🔨 Atualmente, ainda estou em **desenvolvimento**\n"
            f"👑 Fale com minha sensei **Kioyichi** caso tenha alguma dúvida!\n"
            f"⭐  Ora ora ora! (Star Platinum é o melhor 😏)"
        )
            

            estado_bot["energia"] -= 4
            estado_bot["energia"] = max(0, estado_bot["energia"])
            return
            
    # ======= RESPOSTA A REPLIES =======

    if message.reference and message.reference.resolved:
        if message.reference.resolved.author == bot.user:

            async with message.channel.typing():
                await asyncio.sleep(tempo_digitando)

                await message.channel.send(
                    f"{message.author.mention} Posso te ajudar em algo? :3"
                )

                estado_bot["energia"] -= 4
                return

    
    # ======= RESPOSTA RELAÇÃO SOCIYUME =======

    if (
        message.author.id == config.YUME_ID and bot.user in message.mentions and any(conteudo.startswith(frase) for frase in ["eu te amo", "te amo"])
    ):
        async with message.channel.typing():
            await asyncio.sleep(tempo_digitando)

        await message.reply(
            f"Eu também te amo, {message.author.mention} 💙"
        )

        estado_bot["energia"] -= 3
        estado_bot["energia"] = max(0, estado_bot["energia"])
        return
    
    # ======= RESPOSTA A TENDI =======

    if conteudo in ["tendi", "tendeu", "entendi"]:
        async with message.channel.typing():
            await asyncio.sleep(tempo_digitando)
            await message.reply("eu entendi também, eu acho")
            return

        estado_bot["energia"] -= 2
        estado_bot["energia"] = max(0, estado_bot["energia"])
        return
    
    await bot.process_commands(message)

# ======= UTILÁRIOS =======

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

# ======= INICIALIZAÇÃO =======

if __name__ == "__main__":
    TOKEN = os.environ["TOKEN"]

asyncio.run(main())

bot.run(TOKEN)

    