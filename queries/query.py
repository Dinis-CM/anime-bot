import requests
import json
from utilities import load_query, get_all_users

def query(query_name, variables):
    API = "https://graphql.anilist.co"
    print(f"[DEBUG] Loading query '{query_name}' with variables: {variables}")
    query = load_query(query_name)
    response = requests.post(API, json={"query": query, "variables": variables})
    print(f"[DEBUG] Received response with status code: {response.status_code}")
    return response.status_code, response.text, response.json()
    

def get_media_list_from_username(username):
    API = "https://graphql.anilist.co"
    query = load_query("media_list_from_username")
    variables = {"username": username} 
    response = requests.post(API, json={"query": query, "variables": variables})
    if response.status_code != 200:
        print(response.text)
    response.raise_for_status()
    with open("debug_media_list_response.json", "w") as debug_file:
        json.dump(response.json(), debug_file, indent=2)
    anime_data = response.json()['data']['animeList']['lists']
    # Flatten all entries in the anime and manga lists
    anime_entries = [entry for lst in anime_data for entry in lst.get('entries', [])]
    manga_data = response.json()['data']['mangaList']['lists']
    manga_entries = [entry for lst in manga_data for entry in lst.get('entries', [])]
    
    return anime_entries, manga_entries


def get_media_list_from_id(user_id):
    API = "https://graphql.anilist.co"
    query = load_query("media_list_from_id")
    variables = {"userId": user_id}
    response = requests.post(API, json={"query": query, "variables": variables})
    if response.status_code != 200:
        print(response.text)
    response.raise_for_status()
    anime_data = response.json()['data']['animeList']['lists']
    # Flatten all entries in the anime and manga lists
    anime_entries = [entry for lst in anime_data for entry in lst.get('entries', [])]
    manga_data = response.json()['data']['mangaList']['lists']
    manga_entries = [entry for lst in manga_data for entry in lst.get('entries', [])]
    user_data = response.json()['data']['user']
    return anime_entries, manga_entries, user_data
