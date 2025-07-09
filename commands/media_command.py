import discord
from queries import get_media_details, get_all_users_media_details
from embeds import send_media_message

async def media_command(interaction: discord.Interaction, title: str, category: str):

    await interaction.response.defer()

    media_search_results = get_media_details(title, category)
    
    if not media_search_results:
        await interaction.response.send_message(f"No results found for the title: {title}")
        return
    
    users_search_results = get_all_users_media_details(media_search_results['id'], category)
   
    await send_media_message(interaction, media_search_results, users_search_results, category)