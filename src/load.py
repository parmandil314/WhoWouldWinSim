import json
import os
import copy
import numpy as np

import tcod

import skills
import fighter
import dice
import arena

from pathlib import Path


GLOBALS = {
    "numpy": np,
    "tcod": tcod,
    "dice": dice,
    "fighter": fighter,
    "arena": arena
}


def load_tiles(arena_folder_path: str):
    tiles = []
    for entry in Path(f"{arena_folder_path.removesuffix("/")}/tiles").iterdir():
        if entry.name.endswith(".json"):
            with open(entry, "r") as f:
                tile = load_tile(entry.name.removesuffix(".json"), f.read())
                if tile is not None:
                    tiles.append(tile)
    return tiles


def load_tile(filename: str, json_text: str):
    json_dict: dict = json.loads(json_text)

    import arena

    try:
        walk_cost = json_dict["walk_cost"]
        try:
            damage = json_dict["damage"]
        except:
            damage = 2 if walk_cost == 0 else 0
        return arena.Tile(json_dict["name"], filename, json_dict["char"], json_dict["fg"], json_dict["bg"], walk_cost, damage, json_dict["is_opaque"])
    except:
        return None


def load_arena_names() -> dict[str, str]:

    names_dict: dict[str, str] = {}
    for folder_entry in Path("res/arenas").iterdir():
        if folder_entry.is_dir():
            for entry in folder_entry.iterdir():
                if entry.is_file() and entry.name.endswith(".json"):
                    with open(entry, "r") as f:
                        json_dict = json.load(f)
                        try:
                            names_dict[json_dict["name"]] = str(entry.resolve())
                        except:
                            continue
    return names_dict


def load_arena(filename: str, a_name: str, b_name: str) -> arena.Arena:
    with open(filename, "r") as f:
        json_dict: dict = json.load(f)
        new_arena = arena.Arena(json_dict["name"], str(Path(filename).resolve().parent), json_dict["width"], json_dict["height"], False, a_name, b_name)
        
        a_start = json_dict.get("a_start")
        if a_start:
            new_arena.a_start = tuple(a_start)
        
        b_start = json_dict.get("b_start")
        if b_start:
            new_arena.b_start = tuple(b_start)
        
        tiles: list[int] = json_dict["tiles"]
        new_arena.tiles = np.reshape(tiles, (new_arena.height, new_arena.width))

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
        exec(python_text, GLOBALS, local_namespace)
        return local_namespace["execute"]
    except:
        return None


def load_weapons():

    weapons: dict[str, fighter.Weapon] = {}
    for entry in Path("res/weapons").iterdir():
        if entry.name.endswith(".json"):
            with entry.open() as f:
                new_weapon = load_weapon(f.read())
            if new_weapon is not None:
                weapons[new_weapon.name] = new_weapon
    return weapons


def load_weapon(json_text: str):
    json_dict: dict = json.loads(json_text)
    try:
        return fighter.Weapon(json_dict["name"], json_dict["skill"], json_dict["num_attacks"], json_dict["range"],
                            json_dict["num_dice"], json_dict["dice_sides"], json_dict["modifier"])
    except:
        return None


def load_fighters() -> list[fighter.Fighter]:
    
    abilities = load_abilities()
    weapons = load_weapons()
    fighters = []
    for possible_folder in Path("res/fighters").iterdir():
        if possible_folder.is_dir():
            for entry in possible_folder.iterdir():
                if entry.name.endswith(".json"):
                    with entry.resolve().open() as f:
                        new_fighter = load_fighter(f.read(), possible_folder, abilities, weapons)
                        if new_fighter is not None:
                            fighters.append(new_fighter)
    return fighters


def load_fighter(json_text: str, dir: Path, abilities: dict, weapons: dict) -> fighter.Fighter | None:

    json_dict: dict = json.loads(json_text)
    
    try:
        new_fighter = fighter.Fighter(json_dict["name"], json_dict["is_character"])

        char = json_dict.get("char")
        if char:
            new_fighter.char = char
        
        new_fighter.hp = json_dict["hp"]
        new_fighter.max_hp = int(new_fighter.hp)
        new_fighter.build = json_dict["build"]
        new_fighter.db = json_dict["db"]
        new_fighter.armor = json_dict["armor"]
        new_fighter.dodge = json_dict["dodge_if"]
        new_fighter.move_rate = json_dict["move_rate"]

        for name in json_dict["abilities"]:
            new_fighter.abilities[name] = abilities[name]
        
        for name in json_dict["weapons"]:
            new_fighter.weapons[name] = weapons[name]

        with open(f"{dir}/{json_dict["choose_ability_func"]}", "r") as f:
            local_namespace = {}
            try:
                exec(f.read(), GLOBALS, local_namespace)
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