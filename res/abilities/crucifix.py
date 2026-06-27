import fighter
from arena import Arena
import dice

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter):
    
    if defender.name != "Dracula":
        return
    
    arena.print(f"{attacker.name} holds up a crucifix!", (255, 255, 0))

    success = dice.general_roll(defender, "CON")
    if success != 1:
        amount = int(defender.hp * 0.75)
        if attacker.max_hp < attacker.hp + amount:
            arena.print(f"{attacker.name} regains all their HP!", (0, 0, 255))
            attacker.hp = attacker.max_hp
        else:
            arena.print(f"{attacker.name} regains {amount} HP!", (0, 0, 255))
            attacker.hp += amount
        
        arena.print(f"{defender.name} is burned by the crucifix!", (0, 0, 255))
        defender.take_damage(amount)
    else:
        arena.print(f"{defender.name} somehow avoids being burned!", (255, 0, 0))