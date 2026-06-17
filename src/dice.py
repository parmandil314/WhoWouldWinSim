import random
import re

import skills


def roll(notation):
    match = re.match(r'(\d+)d(\d+)(\+?(\d+)?)', notation)
    if not match:
        raise ValueError("Invalid dice notation")

    num_dice = int(match.group(1))
    sides = int(match.group(2))
    try:
        modifier = int(match.group(3))
    except ValueError:
        modifier = 0

    return sum(random.randint(1, sides) for _ in range(num_dice)) + modifier


"""
Skill roll, attack roll, etc.
"""
def general_roll(fighter, skill):
    return roll(f"1d100+{fighter.skills[skill] if skill in fighter.skills.keys() else skills.DEFAULT_SKILLS[skill]}")