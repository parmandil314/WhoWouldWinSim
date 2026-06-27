import fighter
from arena import Arena
import dice

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter):
    
    if defender.name != "Dracula":
        return
    
    success = dice.general_roll(attacker, "DEX")
    if success:

        arena.print(f"{attacker.name} holds up their crucifix!", (0, 0, 255))
        amount = int(defender.hp * 0.75)
        if attacker.max_hp < attacker.hp + amount:
            arena.print(f"{attacker.name} regains all their HP!", (0, 0, 255))
            attacker.hp = attacker.max_hp
        else:
            arena.print(f"{attacker.name} regains {amount} HP!", (0, 0, 255))
            attacker.hp += amount
        
        arena.print(f"{defender.name} is burnt by the crucifix!", (0, 0, 255))
        defender.take_damage(amount)
    else:
        arena.print(f"{defender.name} avoids a splash of holy water from {attacker.name}!", (255, 0, 0))