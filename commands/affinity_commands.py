from queries import query
from utilities import get_users_correlation, get_user_id, get_all_users
from embeds import error_embed, affinity_embed

async def affinity_command(interaction):

    await interaction.response.defer()

    affinity=[]
    all_ids = get_all_users()

    user_id = get_user_id(interaction.user.id)
    
    query_name = "media_list"
    variables = {"userId": user_id}
    status_code, response_text, response_json = query(query_name, variables)

    if status_code != 200:
        embed = error_embed(status_code, response_text)
        await interaction.followup.send(embed=embed)
        return

    
    anime_data_1 = response_json['data']['animeList']['lists']
    manga_data_1 = response_json['data']['mangaList']['lists']
    user_data_1 = response_json['data']['user']
    
    # Flatten all entries in the anime and manga lists
    anime_list_1 = [entry for lst in anime_data_1 for entry in lst.get('entries', [])]
    manga_list_1 = [entry for lst in manga_data_1 for entry in lst.get('entries', [])]
    
    for anilist_id in all_ids:
        if anilist_id != user_id:
            
            query_name = "media_list"
            variables = {"userId": anilist_id}
            status_code, response_text, response_json = query(query_name, variables)

            if status_code != 200:
                embed = error_embed(status_code, response_text)
                await interaction.followup.send(embed=embed)
                return
           
            anime_data_2 = response_json['data']['animeList']['lists']
            manga_data_2 = response_json['data']['mangaList']['lists']
            user_data_2 = response_json['data']['user']
            
            # Flatten all entries in the anime and manga lists
            anime_list_2 = [entry for lst in anime_data_2 for entry in lst.get('entries', [])]
            manga_list_2 = [entry for lst in manga_data_2 for entry in lst.get('entries', [])]

            anime_correlation, manga_correlation, total_correlation, number_common_anime, number_common_manga = get_users_correlation(
                anime_list_1, anime_list_2, manga_list_1, manga_list_2
            )
            
            affinity.append({
                "user": user_data_2['name'],
                "anime_correlation": anime_correlation,
                "manga_correlation": manga_correlation,
                "total_correlation": total_correlation,
                "number_common_anime": number_common_anime,
                "number_common_manga": number_common_manga
            })

    print(f"Affinity results for {user_data_1['name']}: {len(affinity)} users found")
    embed = affinity_embed(affinity, user_data_1['name'])   
    await interaction.followup.send(embed=embed)
    

async def compare_users_command(interaction, username_1, username_2):
    
    await interaction.response.defer()

    affinity=[]

    query_name = "media_list"
    
    variables_1 = {"username": username_1}
    status_code_1, response_text_1, response_json_1 = query(query_name, variables_1)

    variables_2 = {"username": username_2}
    status_code_2, response_text_2, response_json_2 = query(query_name, variables_2)

    if status_code_1 != 200 or status_code_2 != 200:
        embed = error_embed(status_code_1, response_text_1) if status_code_1 != 200 else error_embed(status_code_2, response_text_2)
        await interaction.followup.send(embed=embed)
        return

    anime_data_1 = response_json_1['data']['animeList']['lists']
    manga_data_1 = response_json_1['data']['mangaList']['lists']
    anime_data_2 = response_json_2['data']['animeList']['lists']
    manga_data_2 = response_json_2['data']['mangaList']['lists']
    
    # Flatten all entries in the anime and manga lists
    anime_list_1 = [entry for lst in anime_data_1 for entry in lst.get('entries', [])]
    manga_list_1 = [entry for lst in manga_data_1 for entry in lst.get('entries', [])]
    anime_list_2 = [entry for lst in anime_data_2 for entry in lst.get('entries', [])]
    manga_list_2 = [entry for lst in manga_data_2 for entry in lst.get('entries', [])]

    anime_correlation, manga_correlation, total_correlation, number_common_anime, number_common_manga = get_users_correlation(anime_list_1, anime_list_2, manga_list_1, manga_list_2)

    affinity.append({
        "user": username_2,
        "anime_correlation": anime_correlation,
        "manga_correlation": manga_correlation,
        "total_correlation": total_correlation,
        "number_common_anime": number_common_anime,
        "number_common_manga": number_common_manga
    })

    embed = affinity_embed(affinity, username_1)
    await interaction.followup.send(embed=embed)
