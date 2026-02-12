import discord
from discord.ext import commands
from discord import app_commands

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@commands.hybrid_command(name="daily", description="Resgata seu salário da CLT.")
async def daily(self, ctx):
    await ctx.send("Salário caiu, trabalhador. 💸")

async def setup(bot):
    await bot.add_cog(Economy(bot))