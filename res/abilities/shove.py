import fighter
import arena
import dice

def execute(fighter_arena: arena.Arena, attacker: fighter.Fighter, defender: fighter.Fighter):
    if dice.roll_maneuver(attacker, defender, "brawl"):
        x, y, _ = fighter_arena.nearest_wall(*defender.pos)
        wall_pos = (x, y)
        path = fighter_arena.shortest_path(defender.pos, wall_pos, [attacker.pos])

        for step in path:
            a_present = attacker.pos[0] == step[0] and attacker.pos[1] == step[1]
            d_present = defender.pos[0] == step[0] and defender.pos[1] == step[1]
            fighter_present = a_present or d_present
            is_walkable = fighter_arena.tile_type(*step).walk_cost > 0

            if fighter_present:
                continue
            elif is_walkable:
                fighter_arena.print(f"{attacker.name} shoves {defender.name}!")
                defender.pos = step
                return
            else:
                tile_type = fighter_arena.tile_type(*step)
                fighter_arena.print(f"{attacker.name} shoves {defender.name} into the {tile_type.name}!")
                defender.take_damage(tile_type.damage)
                return
    else:
        fighter_arena.print(f"{attacker.name} fails to move {defender.name}!")