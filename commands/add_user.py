import discord
from queries import query
from utilities import save_user_ids, user_exists
from embeds import *

async def add_user_command(interaction: discord.Interaction, username: str):
    
    await interaction.response.defer(ephemeral=True)

    discord_user_id = interaction.user.id

    query_name = "username"
    variables = {"name": username}
    status_code, response_text, response_json = query(query_name, variables)

    if status_code != 200:
        embed = error_embed(status_code, response_text)
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    anilist_user_id = response_json['data']['User']['id']

    if not user_exists(discord_user_id):
        save_user_ids(discord_user_id, anilist_user_id)
        embed = success_embed(discord_user_id, anilist_user_id, username)
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = duplicate_user_embed(discord_user_id, anilist_user_id, username)
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

   