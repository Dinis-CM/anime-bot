import discord

def error_embed(error_code, error_message):
    print(f"[DEBUG] Creating error embed for code: {error_code}")

    if error_code == 429:
        title = "SLOW THE FUCK DOWN!"
        description = "Error 429: Too Many Requests"
    elif error_code == 404:
        title = "I'M LOST"
        description = "Error 404: Not Found"
    else:
        title = "I AM A BAD BOT AND I HAVE FAILED!"
        description = f"Error {error_code}: {error_message}"
   
    embed = discord.Embed(
            title=title,
            description=description,  
            color=discord.Color.red()
        )
    print("[DEBUG] Embed created")
    return embed
