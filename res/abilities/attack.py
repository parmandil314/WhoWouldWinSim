import fighter
from arena import Arena
import dice

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter):    
    
    if attacker.action_taken:
        return
    
    weapon = attacker.equipped_weapon
    if weapon is None:
        weapon = fighter.DEFAULT_MELEE_WEAPON
        
    if not attacker.in_range(defender, weapon.range):
        return

    if eval(defender.dodge):

        attacker_success = dice.general_roll(attacker, "brawl")
        defender_success = dice.general_roll(defender, "dodge")

        if attacker_success > defender_success:
            damage = weapon.roll_damage()
            if weapon.range == 0:
                damage += attacker.db
            
            arena.print(f"{attacker.name} hits {defender.name}!", (255, 0, 0))
            defender.take_damage(damage)
            arena.print(" ", (0, 0, 0))
        elif defender_success <= attacker_success:
            arena.print(f"{defender.name} dodges an attack from {attacker.name}!", (0, 255, 0))
            arena.print(" ", (0, 0, 0))
    else:
        attacker_success = dice.general_roll(attacker, "brawl")
        defender_success = dice.general_roll(defender, "brawl")

        if attacker_success > defender_success:
            damage = weapon.roll_damage()
            if weapon.range == 0:
                damage += attacker.db
            arena.print(f"{attacker.name} hits {defender.name}!", (255, 0, 0))
            defender.take_damage(damage)
            arena.print(" ", (0, 0, 0))
        
        elif defender_success > attacker_success:

            arena.print(f"{defender.name} avoids an attack from {attacker.name}!", (0, 0, 255))
            if weapon.range == 0:
                damage = dice.roll(1, 3) + defender.db
                arena.print(f"{defender.name} fights back, dealing {damage} damage!", (255, 0, 0))
                attacker.take_damage(damage, False)
                arena.print(" ", (0, 0, 0))
            
        else:
            arena.print(f"{attacker.name} fails to effectively hit {defender.name}, dealing no damage!", (100, 100, 100))
            arena.print(" ", (0, 0, 0))
        
    attacker.action_taken = True