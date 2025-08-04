import discord
from queries.query import *
from utilities.database import save_user_ids, user_exists
from embeds import *

async def add_user_command(interaction: discord.Interaction, username: str):
    
    await interaction.response.defer(ephemeral=True)

    discord_user_id = interaction.user.id
    anilist_user_id = get_user_id_from_username(username)
    
    if not anilist_user_id:
        await interaction.followup.send(f"User {username} not found on Anilist.", ephemeral=True)
        return
    
    if not user_exists(discord_user_id):
        save_user_ids(discord_user_id, anilist_user_id)
        await interaction.followup.send(f"User {username} added successfully!", ephemeral=True)
    else:
        await interaction.followup.send(f"You are already registered.", ephemeral=True)
        return

   