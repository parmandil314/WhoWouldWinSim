import json
import os
import copy

import skills
import fighter
import dice

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
        exec(python_text, {"dice": dice, "fighter": fighter}, local_namespace)
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
        new_fighter.hp = json_dict["hp"]
        new_fighter.armor = json_dict["armor"]
        new_fighter.dodge_if = json_dict["dodge_if"]

        for name in json_dict["abilities"]:
            new_fighter.abilities[name] = abilities[name]

        with open(f"res/fighters/{json_dict["choose_ability_func"]}", "r") as f:
            local_namespace = {}
            try:
                exec(f.read(), {}, local_namespace)
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