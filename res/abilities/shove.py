import fighter
import arena
import dice

def execute(fighter_arena: arena.Arena, attacker: fighter.Fighter, defender: fighter.Fighter):

    try:
        if dice.roll_maneuver(attacker, defender, "brawl"):
            path = fighter_arena.nearest_wall(*defender.pos)
            step = path[0]
            if len(path) > 1:

                a_present = attacker.pos[0] == step[0] and attacker.pos[1] == step[1]
                if a_present:
                    fighter_arena.print(f"{attacker.name} shoves {defender.name}!", (255, 255, 0))
                    attacker_pos = (attacker.pos[0], attacker.pos[1])
                    defender_pos = (defender.pos[0], defender.pos[1])
                    attacker.pos = defender_pos
                    defender.pos = attacker_pos
                else:
                    fighter_arena.print(f"{attacker.name} shoves {defender.name}!", (255, 255, 0))
                    defender.pos = step
                    return
            else:
                tile_type = fighter_arena.tile_type(*step)
                fighter_arena.print(f"{attacker.name} shoves {defender.name} into the {tile_type.name}!", (255, 0, 0))
                defender.take_damage(tile_type.damage)
            
        else:
            fighter_arena.print(f"{attacker.name} fails to move {defender.name}!", (100, 100, 100))
    except Exception as e:
        print(f"shove.py: {e}")