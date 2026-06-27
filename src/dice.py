import random

import skills


def roll(num_dice: int, sides: int, modifier: int = 0):

    if sides == 0:
        return 0
    return sum([random.randint(1, sides) for _ in range(num_dice)]) + modifier


"""
Skill roll, attack roll, etc.
"""
def general_roll(fighter, skill, num_bonuses=0, num_penalties=0):

    result = roll(1, 100)
    for _ in range(num_bonuses):
        result -= roll(1, 10)
    for _ in range(num_penalties):
        result += roll(1, 10)
    
    skill_val = fighter.skills[skill] if skill in fighter.skills.keys() else skills.DEFAULT_SKILLS[skill]

    success = 0
    if result <= skill_val // 5:
        success = 1
    elif result <= skill_val // 2:
        success = 2
    elif result <= skill_val:
        success = 3
    
    return success


def roll_maneuver(attacker, defender, skill) -> bool:

    if attacker.build <= defender.build - 3:
        return False

    success = 0
    if attacker.build == defender.build - 1:
        success = general_roll(attacker, skill, num_penalties=1)
    elif attacker.build == defender.build - 2:
        success = general_roll(attacker, skill, num_penalties=2)
    else:
        success = general_roll(attacker, skill, num_bonuses=attacker.build - defender.build)
    
    dodging: bool = eval(defender.dodge)
    opposing_success = general_roll(defender, "dodge" if dodging else skill)

    if success > opposing_success:
        return True
    return False
    