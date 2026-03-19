import json
import os

ID_FILE = os.path.join(os.path.dirname(__file__), "ids.json")
NAME_FILE = os.path.join(os.path.dirname(__file__), "usernames.json")


def _load_db(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return {}
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {}

def _save_db(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_user(discord_user_id, anilist_user_id, anilist_username):
    user_id_data = _load_db(ID_FILE)
    user_id_data[str(discord_user_id)] = anilist_user_id
    _save_db(user_id_data, ID_FILE)

    username_data = _load_db(NAME_FILE)
    username_data[str(anilist_user_id)] = anilist_username
    _save_db(username_data, NAME_FILE)

def user_exists(discord_user_id):
    user_id_data = _load_db(ID_FILE)
    return str(discord_user_id) in user_id_data

def get_user_id(discord_user_id):
    user_id_data = _load_db(ID_FILE)
    return user_id_data.get(str(discord_user_id))

def get_all_users():
    user_id_data = _load_db(ID_FILE)
    return list(user_id_data.values())

def update_username(anilist_user_id, anilist_username):
    username_data = _load_db(NAME_FILE)
    username_data[str(anilist_user_id)] = anilist_username
    _save_db(username_data, NAME_FILE)

def get_username(anilist_user_id):
    username_data = _load_db(NAME_FILE)
    return username_data.get(str(anilist_user_id))