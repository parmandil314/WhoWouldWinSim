import fighter
from arena import Arena
import dice

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter):
    
    if defender.name in ("Van Helsing", "Dracula", "Frankenstein's Monster"):
        return
    
    self_success = dice.general_roll(attacker, "POW")
    defender_success = dice.general_roll(defender, "POW")
    if self_success > defender_success and self_success == 1:
        arena.print(f"{attacker.name} bites {defender.name}!", (255, 0, 0))
        damage = defender.hp // 2
        defender.take_damage(damage if damage > 0 else 1, False)
    else:
        arena.print(f"{defender.name} avoids being bitten by {attacker.name}!", (255, 0, 0))