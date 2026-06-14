import json
import os 

game_data = {
    "cash": 1000,
    "unlocked_games": {
        "aviator": False,
        "blackjack": False,
        "poker": False
    },
    "has_made_first_choice": False,
    "max_cash": 1000,
    "music_enabled": True,
    "sound_enabled": True,
    "leaderboard": []
}

game_data = game_data.copy()

def save():
    with open("save_data.json", "w") as f:
        json.dump(game_data, f, indent=4)


def load():
    global game_data
    if os.path.exists("save_data.json"):
        with open("save_data.json", "r") as f:
            loaded_data = json.load(f)
       
            for key, val in game_data.items():
                if key not in loaded_data:
                    loaded_data[key] = val
            game_data = loaded_data
    else:
        game_data = game_data.copy()
        save()