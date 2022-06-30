import json
import os

import text_tools

players = []

for filename in os.listdir("players"):
    with open(os.path.join("players", filename), 'r') as f:
        data = json.load(f)
        players.append(data)



def get_player(id: int)->str:
    name = ""
    for p in players:
        if p["id"] == id:
            name = p["name"]
            break
    return name

def list_players() -> str:

    nameregionSize = 30


    msg_header = "Name" + (" " * (nameregionSize - len("Name"))) + "Level\n"
    msg = ""

    for p in players:
        msg += p["name"] + (" " * (nameregionSize - len(p["name"]))) + str(p["level"]) + "\n"

    if(len(msg_header) >= text_tools.get_text_block_width(msg)):
        msg = text_tools.add_bar(msg_header, "below") + msg
    else:
        msg = msg_header + text_tools.add_bar(msg, "above")

    return msg

print(players)