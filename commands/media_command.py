import discord
from queries import query
from embeds import media_embed
from utilities import get_all_users

# Main command function to fetch media details and user list entries
async def media_command(interaction: discord.Interaction, media_title: str, media_type: str):
   
    # Defer the response to allow time for processing
    await interaction.response.defer()
    
    # Check if media_title is an ID or a name
    if media_title.isdigit():
        media_id = int(media_title)
        variables = {"id": media_id, "type": media_type.upper()}
    else:
        variables = {"search": media_title, "type": media_type.upper()}

    # Query media details from the API
    query_name = "media_details"
    media_status_code, media_response_text, media_response_json = query(query_name, variables)

    # Handle errors in media query
    if media_status_code != 200:
        await interaction.followup.send_message(f"Error {media_status_code} fetching media details: {media_response_text}")
        return

    media_query = media_response_json['data']['Media']

    # Get all users to check their list entries for this media
    user_list = get_all_users()
    user_query = []

    for user_id in user_list:
        query_name = "list_entry_from_media_id"
        variables = {"userId": user_id, "mediaId": media_query['id'], "type": media_type.upper()}
        user_status_code, user_response_text, user_response_json = query(query_name, variables)

        # Handle errors and missing entries
        if user_status_code not in [200, 404]:
            await interaction.followup.send_message(f"Error {user_status_code} fetching user details: {user_response_text}")
            return
        elif user_status_code == 404:
            # User does not have this media in their list
            user_query.append({
                "username": user_response_json['data']['MediaList']['user']['name'],
                "status": "NOT IN LIST",
                "progress": "N/A",
                "score": "N/A",
            })
        else:
            # User has this media in their list, add their details
            user_query.append({
                "username": user_response_json['data']['MediaList']['user']['name'],
                "status": user_response_json['data']['MediaList'].get('status', "NOT IN LIST"),
                "progress": user_response_json['data']['MediaList'].get('progress', "N/A"),
                "score": user_response_json['data']['MediaList'].get('score', 0),
            })

    # Create and send the embed with media and user details
    embed = media_embed(media_query, user_query, media_type)
    await interaction.followup.send(embed=embed)
