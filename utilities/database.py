import json
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "users.json")

def _load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_user_ids(discord_user_id, anilist_user_id):
    data = _load_db()
    data[str(discord_user_id)] = anilist_user_id
    _save_db(data)

def user_exists(discord_user_id):
    data = _load_db()
    return str(discord_user_id) in data

def get_user_id(discord_user_id):
    data = _load_db()
    return data.get(str(discord_user_id))

def get_all_users():
    data = _load_db()
    return list(data.values())