import requests
import json
from utilities.load_query import load_query

def get_username_from_user_id(user_id):
    API = "https://graphql.anilist.co"
    query = load_query("username_from_user_id")
    variables = {"id": user_id}
    response = requests.post(API, json={"query": query, "variables": variables})
    response.raise_for_status()
    username = response.json()['data']['User']['name']
    return username

def get_user_id_from_username(username):
    API = "https://graphql.anilist.co"
    query = load_query("user_id_from_username")
    variables = {"name": username}
    response = requests.post(API, json={"query": query, "variables": variables})
    response.raise_for_status()
    user_id = response.json()['data']['User']['id']
    return user_id
    

def get_media_details(title, category):
    API = "https://graphql.anilist.co"
    query_id = load_query("media_details_from_title")
    variables_id = {"search": title, "type": category.upper()}
    response = requests.post(API, json={"query": query_id, "variables": variables_id})
    if response.status_code != 200:
        print(response.text)
    response.raise_for_status()
    return response.json()['data']['Media']

def get_all_users_media_details(media_id, category):
    API = "https://graphql.anilist.co"

    with open("users.json", "r") as f:
        users = json.load(f)

    results = []
   
    for _, anilist_id in users.items():
        query = load_query("list_entry_from_media_id")
        variables = {"userId": anilist_id, "mediaId": media_id, "type": category.upper()}
        response = requests.post(API, json={"query": query, "variables": variables})
        if response.status_code == 404:
            results.append({
                "username": get_username_from_user_id(anilist_id),
                "status": "NOT IN LIST",
                "progress": "N/A",
                "score": "N/A",
            })
        else: 
            response.raise_for_status()
            data = response.json()['data']['MediaList']
            print(f"Data found for user ID: {anilist_id}")
            results.append({
                "username": data['user']['name'],
                "status": data.get('status', "NOT IN LIST"),
                "progress": data.get('progress', "N/A"),
                "score": data.get('score', "N/A"),
            })
    return results