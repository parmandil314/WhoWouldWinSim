import fighter
from arena import Arena
import dice

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter) -> int:    
    
    if eval(defender.dodge_if):

        attacker_success = dice.general_roll(attacker, "brawl")
        defender_success = dice.general_roll(defender, "dodge")

        if attacker_success > defender_success:
            damage = dice.roll(1, 3) + dice.roll(1, attacker.db) - defender.armor
            defender.take_damage(damage)
            print(f"{attacker.name} punches {defender.name}!")
            return damage
        elif defender_success <= attacker_success:
            print(f"{defender.name} dodges a punch from {attacker.name}!")
            return 2
    else:
        attacker_success = dice.general_roll(attacker, "brawl")
        defender_success = dice.general_roll(defender, "brawl")

        if attacker_success > defender_success:
            damage = dice.roll(1, 3) + dice.roll(1, attacker.db) - defender.armor
            defender.take_damage(damage)
            print(f"{attacker.name} punches {defender.name}!")
            return damage
        elif defender_success > attacker_success:
            damage = dice.roll(1, 3) + dice.roll(1, defender.db) - attacker.armor
            print(f"{defender.name} blocks a punch from {attacker.name}!")
            print(f"{defender.name} deals {damage} damage in the process!")
            attacker.take_damage(damage, False)
            return damage
        else:
            print(f"{attacker.name} fails to effectively punch {defender.name}, dealing no damage!")
            return 2
    return 0