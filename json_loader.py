import json


def load_json(file):
    """Load json file"""
    with open(file) as load_file:
        loaded_file = json.load(load_file)
    return loaded_file

def get_account():
    """Retrieves instagram account"""
    json_file = load_json("settings.json")
    accounts = json_file["instagram"]
    return accounts

def get_settings(subreddit):
    """Retrieves settings from json file."""
    settings = load_json("settings.json")

    db_path = settings["db_path"]
    img_path = settings["static_path"]

    return db_path, img_path

