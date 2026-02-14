import discord
from discord.ext import commands
import os
import asyncio
import sqlite3
from datetime import datetime, date
import traceback
import random
import unicodedata

import config

humor = "neutro"
interacoes = 0

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

EMOJIS_IDS = [
    1471976695832641751,
    1471976730250969302,
    1471976677348343880,
    1471976746076213378,
    1471976711418679513
]

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
    
    if message.author.bot:
        return

    conteudo = message.content.lower().strip()
    palavras = conteudo.split()
    humor = humor_do_dia()

    if palavras and palavras[0] == "oi" and bot.user in message.mentions:
                    async with message.channel.typing():
                        await asyncio.sleep(1.5)

                    if message.author.id == config.OWNER_ID:
                        if humor == "motivado":
                            resposta = f"Oi, patroa maravilhosa! Já tô fazendo acima da meta :3"

                        elif humor == "neutro":
                            resposta = f"Oi, patroa. O que manda?"

                        elif humor == "cansado":
                            resposta = f"Bom dia chefe... Você bem que poderia me dar uma folguinha, né? 😴"
                        
                        elif humor == "revoltado":
                            resposta = f"Oi, chefia... Inclusive, sobre o meu salário..."
                        
                        elif humor == "triste":
                            resposta = f"Bom dia, patroa... Espero que seu dia esteja bom, porque o meu já começou meio ruim... 😔"

                        else:
                    
                            if humor == "motivado":
                                resposta = "BOM DIA! Já tô pronto pro expediente! ☀️"
                    
                            elif humor == "neutro":
                                resposta = "Bom dia. O expediente já começou, qual o lanche de hoje?"

                            elif humor == "cansado":
                                resposta = "Bom dia... já? Ainda tô com sono... 😴"
                    
                            elif humor == "revoltado":
                                resposta = "Bom dia só se for pra você, porque o dia tá uma droga. 😡"
                            elif humor == "triste":
                                resposta = "Bom dia... se é que dá pra chamar isso de dia... 😔"

                                await message.reply(resposta)
                                return
                            
                            await bot.process_commands(message)


                
    if message.author.bot:
        return
    
    if message.author.id == config.YUME_ID and bot.user in message.mentions:
        conteudo = message.content.lower()
        conteudo = remover_acentos(conteudo)

        if "e o salario" in conteudo:
            async with message.channel.typing():
                await asyncio.sleep(2)
                await message.reply(
                    "O salário tá atrasado, Yume. 😔"
                )


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

def humor_do_dia():
    hoje = date.today()

    random.seed(hoje.toordinal())
    return random.choice(HUMORES)


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

    