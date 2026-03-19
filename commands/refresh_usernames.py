from utilities.database import get_all_users, update_username
from queries.query import query

def refresh_usernames():

    user_list = get_all_users()

    for anilist_user_id in user_list:
        query_name = "username"
        query_variables = {"id": anilist_user_id}
        status_code, _, response_json = query(query_name, query_variables)
        if status_code == 200:
            print(f"Updating username for Anilist ID: {anilist_user_id}")
            anilist_username = response_json['data']['User']['name']
            update_username(anilist_user_id, anilist_username)