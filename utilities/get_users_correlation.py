from scipy.stats import pearsonr

def get_users_correlation(username1_anime_entries, username2_anime_entries,username1_manga_entries, username2_manga_entries):
    

    # Filter out entries with score == 0 or status == 'PLANNING'
    filtered_anime_1 = [entry for entry in username1_anime_entries if entry.get('score', 0) != 0 and entry.get('status') != 'PLANNING']
    filtered_anime_2 = [entry for entry in username2_anime_entries if entry.get('score', 0) != 0 and entry.get('status') != 'PLANNING']
    filtered_manga_1 = [entry for entry in username1_manga_entries if entry.get('score', 0) != 0 and entry.get('status') != 'PLANNING']
    filtered_manga_2 = [entry for entry in username2_manga_entries if entry.get('score', 0) != 0 and entry.get('status') != 'PLANNING']

    # Find common anime and manga IDs
    common_anime_ids = set(entry['mediaId'] for entry in filtered_anime_1) & set(entry['mediaId'] for entry in filtered_anime_2)
    common_manga_ids = set(entry['mediaId'] for entry in filtered_manga_1) & set(entry['mediaId'] for entry in filtered_manga_2)

    # Get common entries, sorted by media id for alignment
    common_anime_1 = sorted([entry for entry in filtered_anime_1 if entry['mediaId'] in common_anime_ids], key=lambda x: x['mediaId'])
    common_anime_2 = sorted([entry for entry in filtered_anime_2 if entry['mediaId'] in common_anime_ids], key=lambda x: x['mediaId'])
    common_manga_1 = sorted([entry for entry in filtered_manga_1 if entry['mediaId'] in common_manga_ids], key=lambda x: x['mediaId'])
    common_manga_2 = sorted([entry for entry in filtered_manga_2 if entry['mediaId'] in common_manga_ids], key=lambda x: x['mediaId'])

    # Align scores by media id
    anime_dict_1 = {entry['mediaId']: entry.get('score') for entry in common_anime_1}
    anime_dict_2 = {entry['mediaId']: entry.get('score') for entry in common_anime_2}
    common_ids = set(anime_dict_1) & set(anime_dict_2)
    anime_scores_1 = [anime_dict_1[mid] for mid in common_ids]
    anime_scores_2 = [anime_dict_2[mid] for mid in common_ids]

    manga_dict_1 = {entry['mediaId']: entry.get('score') for entry in common_manga_1}
    manga_dict_2 = {entry['mediaId']: entry.get('score') for entry in common_manga_2}
    common_ids = set(manga_dict_1) & set(manga_dict_2)
    manga_scores_1 = [manga_dict_1[mid] for mid in common_ids]
    manga_scores_2 = [manga_dict_2[mid] for mid in common_ids]

    total_scores_1 = anime_scores_1 + manga_scores_1
    total_scores_2 = anime_scores_2 + manga_scores_2

    # Calculate correlations, handle cases with insufficient data
    anime_correlation = pearsonr(anime_scores_1, anime_scores_2)[0] if len(anime_scores_1) > 1 else 0
    manga_correlation = pearsonr(manga_scores_1, manga_scores_2)[0] if len(manga_scores_1) > 1 else 0
    if len(total_scores_1) > 1:
        total_correlation = pearsonr(total_scores_1, total_scores_2)[0]
    else:
        total_correlation = 0
    return anime_correlation, manga_correlation, total_correlation, len(anime_scores_1), len(manga_scores_1)