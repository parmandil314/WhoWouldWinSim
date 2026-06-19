import json
import os
import copy
import numpy as np

import tcod

import skills
import fighter
import dice
import arena


globals_dict = {
    "numpy": np,
    "tcod": tcod,
    "dice": dice,
    "fighter": fighter,
    "arena": arena
}


def load_tiles():
    tiles = []
    for entry in os.listdir("res/tiles"):
        if entry.endswith(".json"):
            with open(f"res/tiles/{entry}", "r") as f:
                tile = load_tile(entry.removesuffix(".json"), f.read())
                if tile is not None:
                    tiles.append(tile)
    return tiles


def load_tile(filename: str, json_text: str):
    json_dict = json.loads(json_text)

    import arena

    try:
        return arena.Tile(json_dict["name"], filename, json_dict["char"], json_dict["fg"], json_dict["bg"], json_dict["walk_cost"])
    except:
        return None


def load_arena_names() -> dict[str, str]:

    names_dict = {}
    for entry in os.listdir("res/arenas"):
        if entry.endswith(".json"):
            with open(f"res/arenas/{entry}", "r") as f:
                json_dict = json.load(f)
                try:
                    names_dict[json_dict["name"]] = f"res/arenas/{entry}"
                except:
                    continue
    return names_dict


def load_arena(filename: str) -> arena.Arena:
    with open(filename, "r") as f:
        json_dict: dict = json.load(f)
        new_arena = arena.Arena(json_dict["name"], json_dict["width"], json_dict["height"])
        
        a_start = json_dict.get("a_start")
        if a_start:
            new_arena.a_start = tuple(a_start)
        
        b_start = json_dict.get("b_start")
        if b_start:
            new_arena.b_start = tuple(b_start)
        
        tiles: list[int] = json_dict["tiles"]
        new_arena.tiles = np.reshape(tiles, (new_arena.width, new_arena.height))

        return new_arena


def load_abilities():
    abilities = {}

    for entry in os.listdir("res/abilities"):
        if entry.endswith(".py"):
            with open(f"res/abilities/{entry}", "r") as f:
                new_ability = load_ability(f.read())
                if new_ability is not None:
                    abilities[entry.removesuffix(".py")] = new_ability
    
    return abilities


def load_ability(python_text: str):

    local_namespace = {}
    try:
        exec(python_text, globals_dict, local_namespace)
        return local_namespace["execute"]
    except:
        return None


def load_fighters() -> list[fighter.Fighter]:
    
    abilities = load_abilities()
    fighters = []
    for entry in os.listdir("res/fighters"):
        if entry.endswith(".json"):
            with open(f"res/fighters/{entry}", "r") as f:
                new_fighter = load_fighter(f.read(), abilities)
                if new_fighter is not None:
                    fighters.append(new_fighter)

    return fighters


def load_fighter(json_text: str, abilities: dict) -> fighter.Fighter | None:

    json_dict: dict = json.loads(json_text)
    
    try:
        new_fighter = fighter.Fighter(json_dict["name"], json_dict["is_character"])
    except:
        return None
    
    """
    try:
        limbs: list[dict] = json_dict["limbs"]
        for limb_dict in limbs:
            limb = Limb(limb_dict["name"], limb_dict["hp"])
            new_fighter.limbs.append(limb)
    except:
        pass
    """

    try:
        
        char = json_dict.get("char")
        if char:
            new_fighter.char = char

        new_fighter.speed = json_dict["speed"]
        
        new_fighter.hp = json_dict["hp"]
        new_fighter.armor = json_dict["armor"]
        new_fighter.dodge_if = json_dict["dodge_if"]

        for name in json_dict["abilities"]:
            new_fighter.abilities[name] = abilities[name]

        with open(f"res/fighters/{json_dict["choose_ability_func"]}", "r") as f:
            local_namespace = {}
            try:
                exec(f.read(), globals_dict, local_namespace)
                new_fighter.choose_ability = local_namespace["choose_ability"]
            except:
                return None

        new_fighter.skills = copy.copy(skills.DEFAULT_SKILLS)
        for skill in json_dict["skills"].keys():
            new_fighter.skills[skill] = json_dict["skills"][skill]
        
        for attribute in json_dict["attributes"].keys():
            new_fighter.attributes[attribute] = json_dict["attributes"][attribute]
    except:
        return None

    return new_fighter