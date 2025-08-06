import discord
import json

def error_embed(error_code, error_message):
    print(f"[DEBUG] Creating error embed for code: {error_code}")

    try:
        data = json.loads(error_message)
        real_message = data["errors"][0]["message"]
    except Exception:
        real_message = error_message

    match error_code:
        case 400:
            title = "WHOEVER DID THIS PROGRAM CAN'T CODE FOR SHIT!"
        case 403:
            title = "LISTEN HERE, IT'S NOT ME, IT'S ANILIST FAULT!"
        case 404:
            title = "I'M LOST! :)"
        case 429:
            title = "SLOW THE FUCK DOWN!"
        case _:
            title = "I AM A BAD BOT AND I HAVE FAILED!"
    

    description = f"Error {error_code}: {real_message}"
   
    embed = discord.Embed(
            title=title,
            description=description,  
            color=discord.Color.red()
        )
    print("[DEBUG] Embed created")
    return embed
