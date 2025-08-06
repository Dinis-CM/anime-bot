import os
import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
from commands import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_IDS = os.getenv('GUILD_IDS').split(',')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
guilds = [discord.Object(id=int(gid.strip())) for gid in GUILD_IDS]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    for guild in guilds:
        await bot.tree.sync(guild=guild)

@bot.tree.command(
    name="add-user",
    description="Adds user to registered users in bot",
    guilds=guilds
)
@app_commands.describe(username="Anilist username")
async def add_user(interaction: discord.Interaction, username: str):
    await add_user_command(interaction, username)


@bot.tree.command(
    name="affinity",
    description="Calculates the affinity between the user and all the other users in the guild",
    guilds=guilds
)
@app_commands.describe()
async def affinity(interaction: discord.Interaction):
    await affinity_command(interaction)


@bot.tree.command(
    name="anime",
    description="Get info about an anime",
    guilds=guilds
)
@app_commands.describe(search="Anime title or id to search")
async def anime(interaction: discord.Interaction, search: str):
    await media_command(interaction, search, "ANIME")

@bot.tree.command(
    name="compare-users",
    description="Calculates the affinity between two anilist users",
    guilds=guilds
)
@app_commands.describe(username1="Anilist username", username2="Anilist username")
async def compare_users(interaction: discord.Interaction, username1: str, username2: str):
    await compare_users_command(interaction, username1, username2)

@bot.tree.command(
    name="manga",
    description="Get info about a manga",
    guilds=guilds
)
@app_commands.describe(search="Manga title or id to search")
async def manga(interaction: discord.Interaction, search: str):
    await media_command(interaction, search, "MANGA")

#@bot.tree.command(name="stats", description="Calculates the stats of an user", guild=guild)
#@app_commands.describe(username="Anilist username")
#async def stats(interaction: discord.Interaction, username: str):
#    await stats_command(interaction, username)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
