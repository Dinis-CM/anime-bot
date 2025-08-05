import discord

def success_embed(discord_user_id, anilist_user_id, username):
    embed = discord.Embed(
        title="User Added Successfully",
        description=f"Discord User ID: {discord_user_id}\nAnilist User ID: {anilist_user_id}\nUsername: {username}",
        color=discord.Color.blue()
    )
    return embed

def duplicate_user_embed(discord_user_id, anilist_user_id, username):
    embed = discord.Embed(
        title="User Already Exists",
        description=f"Discord User ID: {discord_user_id}\nAnilist User ID: {anilist_user_id}\nUsername: {username}",
        color=discord.Color.blue()
    )
    return embed