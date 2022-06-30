from cgitb import text
import json
import os

import text_tools

players = []

for filename in os.listdir("players"):
    with open(os.path.join("players", filename), 'r') as f:
        data = json.load(f)
        players.append(data)



def get_player_from_id(id: int):
    player = None
    for p in players:
        if p["id"] == id:
            player = p
            break
    return player


def get_player_from_name(name: str):
    player = None
    for p in players:
        print()
        if name.casefold() in p["name"].casefold():
            player = p
            break
    return player


def list_players() -> str:

    nameregionSize = 30


    msg_header = "Name" + (" " * (nameregionSize - len("Name"))) + "Level"
    msg = ""

    for p in players:
        msg += p["name"] + (" " * (nameregionSize - len(p["name"]))) + str(p["level"]) + "\n"

    if(len(msg_header) >= text_tools.get_text_block_width(msg)):
        msg = text_tools.add_bar(msg_header, "below") + msg
    else:
        msg = msg_header + '\n' + text_tools.add_bar(msg, "above")

    return msg


def print_player(p) -> str:
    stat_block_size = 100
    level_string = "Level " + str(p["level"])


    msg = p["name"] + " " * int(stat_block_size/2 - len(p["name"]) - len(p["title"])/2)
    msg += p["title"] + " " * int(stat_block_size/2 - len(level_string) - len(p["title"])/2)
    msg += level_string

    stat_block_size = len(msg)
    msg = text_tools.add_bar(msg, "below")

    msg += _get_stat_string(p, stat_block_size)

    msg = text_tools.add_bar(msg, "below")
    
    msg += _get_skill_string(p)

    return msg



def _get_stat_string(p, stat_block_width) -> str:

    msg = "|"

    stat_width = int((stat_block_width - 2)/len(p["stats"]))

    remainder = (stat_block_width -2) % stat_width + 1

    print(remainder)

    if remainder % 2 == 0:
        msg += " " * int(remainder/2)
    else:
        msg += " " * (int(remainder/2) + 1)

    print(p["stats"].keys())

    for s in p["stats"].keys():
        stat_string = s[0:3].upper() + " = " + str(p["stats"][s])
        space_width = int((stat_width - 1 - len(stat_string))/2)

        msg += " " * space_width
        msg += stat_string
        msg += " " * space_width
        if s != list(p["stats"].keys())[-1]:
            msg += "|"
        else:
            msg += " " * int(remainder/2) + "|"

    return msg

def _get_skill_string(p) -> str:

    max_len = len("Skills")
    for skill in p["skills"]:
        if len(skill) > max_len:
            max_len = len(skill)

    skill_msg = "| Skills" + " " * (max_len - len("Skills")) + " |" + "\n" 
    skill_msg += "-" * (max_len + 4) + "\n"

    for skill in p["skills"]:
        skill_msg += "| " + skill + " " * (max_len - len(skill)) + " |" + "\n"

    return skill_msg

print(players)