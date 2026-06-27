import fighter
from arena import Arena
import dice

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter):
    
    if defender.name != "Dracula":
        return
    
    success = dice.general_roll(attacker, "DEX")
    if success:
        arena.print(f"{attacker.name} splashes holy water on {defender.name}, burning them!", (0, 0, 255))
        damage = int(defender.hp * 0.75)
        defender.take_damage(damage if damage > 0 else 1, False)
    else:
        arena.print(f"{defender.name} avoids a splash of holy water from {attacker.name}!", (255, 0, 0))