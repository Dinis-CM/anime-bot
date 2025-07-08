import os
import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
server_id = os.getenv('GUILD_ID')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
guild = discord.Object(id=server_id) 

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')
    # Sync the commands with the guild
    await bot.tree.sync(guild=guild)

@bot.tree.command(name="hello", description="hello command", guild=guild)
async def hello(interaction: discord.Interaction):
    embed = discord.Embed(title="The Annie May revival is real!", description="Coming soon...", color=discord.Color.blue())
    embed.set_image(url="https://cdn-images.dzcdn.net/images/cover/7918723b1df0792ea167571d83949b27/0x1900-000000-80-0-0.jpg")
    await interaction.response.send_message(embed=embed)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)