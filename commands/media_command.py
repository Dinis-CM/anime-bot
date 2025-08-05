import discord
from queries import query
from embeds import media_embed, error_embed
from utilities import get_all_users

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
        query_name = "list_entry"
        user_variables = {"userId": user_id, "mediaId": media_query['id'], "type": media_type.upper()}
        user_status_code, user_response_text, user_response_json = query(query_name, user_variables)
        if user_status_code == 200:
            # User has this media in their list, add their details
            user_query.append({
                "username": user_response_json['data']['MediaList']['user']['name'],
                "status": user_response_json['data']['MediaList'].get('status', "NOT IN LIST"),
                "progress": user_response_json['data']['MediaList'].get('progress', "N/A"),
                "score": user_response_json['data']['MediaList'].get('score', 0),
            })
        elif user_status_code == 404:
            
            query_name = "username"
            username_variables = {"id": user_id}
            
            username_status_code, username_response_text, username_response_json = query(query_name, username_variables)

            if username_status_code != 200:
                embed = error_embed(username_status_code, username_response_text)
                await interaction.followup.send(embed=embed)
                return

            user_query.append({
                "username": username_response_json['data']['User']['name'],
                "status": "NOT IN LIST",
                "progress": "N/A",
                "score": "N/A",
            })

        else:
            # Handle other errors
            embed = error_embed(user_status_code, user_response_text)
            await interaction.followup.send(embed=embed)
            return

    # Create and send the embed with media and user details
    embed = media_embed(media_query, user_query, media_type)
    await interaction.followup.send(embed=embed)
