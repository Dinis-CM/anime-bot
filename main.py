import os
import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
from commands import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_ID = os.getenv('GUILD_ID')
ANILIST_API = os.getenv('ANILIST_API')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
guild = discord.Object(id=SERVER_ID) 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    await bot.tree.sync(guild=guild)

@bot.tree.command(name="affinity", description="Calculates the affinity between the user and all the other users in the guild", guild=guild)
@app_commands.describe(username="Anilist username")
async def affinity(interaction: discord.Interaction, username: str):
    await affinity_command(interaction, username)


@bot.tree.command(name="anime", description="Get info about an anime", guild=guild)
@app_commands.describe(title="Anime title to search")
async def anime(interaction: discord.Interaction, title: str):
    await anime_command(interaction, title)

@bot.tree.command(name="compare-users", description="Calculates the affinity between two anilist users", guild=guild)
@app_commands.describe(username1="Anilist username", username2="Anilist username")
async def compare_users(interaction: discord.Interaction, username1: str, username2: str):
    await compare_users_command(interaction, username1, username2)

@bot.tree.command(name="manga", description="Get info about a manga", guild=guild)
@app_commands.describe(title="Manga title to search")
async def manga(interaction: discord.Interaction, title: str):
    await manga_command(interaction, title)

@bot.tree.command(name="stats", description="Calculates the stats of an user", guild=guild)
@app_commands.describe(username="Anilist username")
async def stats(interaction: discord.Interaction, username: str):
    await stats_command(interaction, username)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)





''''
@bot.tree.command(name="hello", description="hello command", guild=guild)
async def hello(interaction: discord.Interaction):
    embed = discord.Embed(title="The Annie May revival is real!", description="Coming soon...", color=discord.Color.blue())
    embed.set_image(url="https://cdn-images.dzcdn.net/images/cover/7918723b1df0792ea167571d83949b27/0x1900-000000-80-0-0.jpg")
    await interaction.response.send_message(embed=embed)


    await interaction.response.defer()  
    try:
        anime_id, _ = get_anime_id(title)
        info = get_anime_details(anime_id)
        anilist_url = f"https://anilist.co/anime/{anime_id}"
        embed = discord.Embed(
            title=info['title']['english'] or info['title']['romaji'],
            url=anilist_url,
            description=info['description'][:4096],  # Discord embed desc limit
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=info['coverImage']['large'])
        embed.add_field(name="Romaji", value=info['title']['romaji'], inline=True)
        embed.add_field(name="Native", value=info['title']['native'], inline=True)
        embed.add_field(name="Format", value=info['format'], inline=True)
        embed.add_field(name="Status", value=info['status'], inline=True)
        embed.add_field(name="Season", value=f"{info['season']} {info['seasonYear']}", inline=True)
        embed.add_field(name="Episodes", value=info['episodes'], inline=True)
        embed.add_field(name="Duration", value=f"{info['duration']} min/ep", inline=True)
        embed.add_field(name="Score", value=f"{info['averageScore']}/100", inline=True)
        embed.add_field(name="Popularity", value=info['popularity'], inline=True)
        embed.add_field(name="Favourited", value=info['favourites'], inline=True)
        embed.add_field(name="Genres", value=', '.join(info['genres']), inline=False)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")
'''
