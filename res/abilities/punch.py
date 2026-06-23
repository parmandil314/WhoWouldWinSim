import fighter
from arena import Arena
import dice

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter):    
    
    if attacker.action_taken:
        return
    
    if eval(defender.dodge):

        attacker_success = dice.general_roll(attacker, "brawl")
        defender_success = dice.general_roll(defender, "dodge")

        if attacker_success > defender_success:
            damage = dice.roll(1, 3) + attacker.db
            arena.print(f"{attacker.name} punches {defender.name}!")
            defender.take_damage(damage)
            arena.print("-", (0, 0, 0))
        elif defender_success <= attacker_success:
            arena.print(f"{defender.name} dodges a punch from {attacker.name}!")
            arena.print("-", (0, 0, 0))
    else:
        attacker_success = dice.general_roll(attacker, "brawl")
        defender_success = dice.general_roll(defender, "brawl")

        if attacker_success > defender_success:
            damage = dice.roll(1, 3) + attacker.db
            arena.print(f"{attacker.name} punches {defender.name}!")
            defender.take_damage(damage)
            arena.print("-", (0, 0, 0))
        elif defender_success > attacker_success:
            damage = dice.roll(1, 3) + defender.db
            arena.print(f"{defender.name} blocks a punch from {attacker.name}!")
            arena.print(f"{defender.name} deals {damage} damage in the process!")
            attacker.take_damage(damage, False)
            arena.print("-", (0, 0, 0))
        else:
            arena.print(f"{attacker.name} fails to effectively punch {defender.name}, dealing no damage!")
            arena.print("-", (0, 0, 0))
    
    attacker.action_taken = True