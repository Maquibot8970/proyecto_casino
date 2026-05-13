import json
import os 

default_data = {
    "cash": 50,
    "has_selected_first_game": False,
    "unlocked_games": {
        "aviator": False,
        "blackjack": False,
        "poker": False
    },
    "leaderboard": []
}

game_data = default_data.copy()

def save():
    with open("save_data.json", "w") as f:
        json.dump(game_data, f, indent=4)


def load():
    global game_data
    if os.path.exists("save_data.json"):
        with open("save_data.json", "r") as f:
            game_data = json.load(f)
    else:
        game_data = default_data.copy()
        save()