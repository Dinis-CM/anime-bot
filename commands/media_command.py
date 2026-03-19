import discord
from queries import query
from embeds import media_embed, error_embed
from utilities import get_all_users, get_username

# Main command function to fetch media details and user list entries
async def media_command(interaction: discord.Interaction, media_title: str, media_type: str):
   
    # Defer the response to allow time for processing
    await interaction.response.defer()
    
    # Check if media_title is an ID or a name
    if media_title.isdigit():
        media_id = int(media_title)
        media_variables = {"id": media_id, "type": media_type.upper()}
    else:
        media_variables = {"search": media_title, "type": media_type.upper()}

    # Query media details from the API
    query_name = "media_details"
    media_status_code, media_response_text, media_response_json = query(query_name, media_variables)

    # Handle errors in media query
    if media_status_code != 200:
        embed = error_embed(media_status_code, media_response_text)
        await interaction.followup.send(embed=embed)
        return

    media_query = media_response_json['data']['Media']

    # Get all users to check their list entries for this media
    user_list = get_all_users()
    user_query = []

    for user_id in user_list:
        
        username = get_username(user_id)
        
        query_name = "list_entry"
        user_variables = {"userId": user_id, "mediaId": media_query['id'], "type": media_type.upper()}
        user_status_code, user_response_text, user_response_json = query(query_name, user_variables)
        
        if user_status_code == 200:
            status = user_response_json['data']['entry'].get('status', "NOT IN LIST")
            progress = user_response_json['data']['entry'].get('progress', "N/A")
            score = user_response_json['data']['entry'].get('score', 0)

        elif user_status_code == 404:
            # User has no entry for this media
            status = "NOT IN LIST"
            progress = "N/A"
            score = 0

        else:
            # Handle other errors
            embed = error_embed(user_status_code, user_response_text)
            await interaction.followup.send(embed=embed)
            return
        
        user_query.append({
            "username": username,
            "status": status,
            "progress": progress,
            "score": score,
        })

    print(user_query)
    # Create and send the embed with media and user details
    embed = media_embed(media_query, user_query, media_type)
    await interaction.followup.send(embed=embed)
