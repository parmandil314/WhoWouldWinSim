import fighter
import dice

def execute(attacker: fighter.Fighter, defender: fighter.Fighter):
    attacker_roll = dice.general_roll(attacker, "brawl")
    attacker_success = 0
    if attacker_roll <= attacker.skills["brawl"]:
        attacker_success = 1
    elif attacker_roll <= attacker.skills["brawl"] // 2:
        attacker_success = 2
    elif attacker_roll <= attacker.skills["brawl"] // 5:
        attacker_success = 3
    
    if exec(defender.dodge_if):
        dodge_roll = dice.general_roll(defender, "brawl")

        defender_success = 0
        if dodge_roll <= defender.skills["dodge"]:
            defender_success = 1
        elif dodge_roll <= defender.skills["dodge"] // 2:
            defender_success = 2
        elif dodge_roll <= defender.skills["dodge"] // 5:
            defender_success = 3

        if attacker_success > defender_success:
            damage = dice.roll("1d3")
            defender.take_damage(damage)
            print(f"{attacker.name} punches {defender.name}!")
        elif defender_success <= attacker_success:
            print(f"{defender.name} dodges a punch from {attacker.name}!")
    else:
        fight_back_roll = dice.general_roll(defender, "brawl")
        defender_success = 0
        if fight_back_roll <= defender.skills["brawl"]:
            defender_success = 1
        elif fight_back_roll <= defender.skills["brawl"] // 2:
            defender_success = 2
        elif fight_back_roll <= defender.skills["brawl"] // 5:
            defender_success = 3

        elif attacker_success > defender_success:
            damage = dice.roll("1d3")
            defender.take_damage(damage)
            print(f"{attacker.name} punches {defender.name}!")
        elif defender_success > attacker_success:
            damage = dice.roll("1d3")
            print(f"{defender.name} blocks a punch from {attacker.name}!")
            print(f"{defender.name} deals {damage} damage in the process!")
            attacker.take_damage(dice.roll("1d3"), False)
        else:
            print(f"{attacker.name} fails to effectively punch {defender.name}, dealing no damage!")