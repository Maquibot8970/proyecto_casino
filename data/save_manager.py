import json
import os 

game_data = {
    "cash": 1000,
    "unlocked_games": {
        "aviator": False,
        "blackjack": False,
        "poker": False
    },
    "has_made_first_choice": False  
}

game_data = game_data.copy()

def save():
    with open("save_data.json", "w") as f:
        json.dump(game_data, f, indent=4)


def load():
    global game_data
    if os.path.exists("save_data.json"):
        with open("save_data.json", "r") as f:
            game_data = json.load(f)
    else:
        game_data = game_data.copy()
        save()