import random
import re

import skills


def roll(num_dice: int, sides: int, modifier: int = 0):

    if sides == 0:
        return 0
    return sum(random.randint(1, sides) for _ in range(num_dice)) + modifier


"""
Skill roll, attack roll, etc.
"""
def general_roll(fighter, skill):
    result = roll(1, 100)
    
    skill_val = fighter.skills[skill] if skill in fighter.skills.keys() else skills.DEFAULT_SKILLS[skill]

    success = 0
    if result <= skill_val // 5:
        success = 1
    elif result <= skill_val // 2:
        success = 2
    elif result <= skill_val:
        success = 3
    
    return success