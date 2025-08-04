from queries.query import get_media_list_from_username, get_media_list_from_id
from utilities.get_users_correlation import get_users_correlation
from utilities.database import get_user_id, get_all_users

async def affinity_command(interaction):

    await interaction.response.defer()

    user_id = get_user_id(interaction.user.id)
  
    anime_lists_1, manga_lists_1, user_data_1 = get_media_list_from_id(user_id)
   
    affinity=[]
    all_ids = get_all_users()
    
    for anilist_id in all_ids:
        if anilist_id != user_id:
            
            anime_lists_2, manga_lists_2, user_data_2 = get_media_list_from_id(anilist_id)
            anime_correlation, manga_correlation, total_correlation, number_common_anime, number_common_manga = get_users_correlation(
                anime_lists_1, anime_lists_2, manga_lists_1, manga_lists_2
            )
            
            affinity.append({
                "user": user_data_2['name'],
                "anime_correlation": anime_correlation,
                "manga_correlation": manga_correlation,
                "total_correlation": total_correlation,
                "number_common_anime": number_common_anime,
                "number_common_manga": number_common_manga
            })

    affinity.sort(key=lambda x: x['total_correlation'], reverse=True)

    message = ""
    for user in affinity:
        message += (
            f"User: {user['user']}\n"
            f"Anime correlation: {user['anime_correlation']:.2f}, "
            f"Manga correlation: {user['manga_correlation']:.2f}, "
            f"Total correlation: {user['total_correlation']:.2f}\n"
            f"Common anime: {user['number_common_anime']}, Common manga: {user['number_common_manga']}\n\n"
        )
    await interaction.followup.send(message)
    

async def compare_users_command(interaction, username1, username2):
    
    await interaction.response.defer()

    anime_lists_1, manga_lists_1 = get_media_list_from_username(username1)
    anime_lists_2, manga_lists_2 = get_media_list_from_username(username2)


    anime_correlation, manga_correlation, total_correlation, number_common_anime, number_common_manga = get_users_correlation(anime_lists_1, anime_lists_2, manga_lists_1, manga_lists_2)

    await interaction.followup.send(
        f"Comparison between {username1} and {username2} completed.\n"
        f"Common anime: {number_common_anime}, Common manga: {number_common_manga}\n"
        f"Anime correlation: {anime_correlation:.2f}, Manga correlation: {manga_correlation:.2f}, "
        f"Total correlation: {total_correlation:.2f}"
    )
