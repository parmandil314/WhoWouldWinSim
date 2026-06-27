import fighter
import arena
import tcod

def execute(fighter_arena: arena.Arena, attacker: fighter.Fighter, defender: fighter.Fighter):
    
    try:        
        costs = [[int(fighter_arena.tile_type(y, x).walk_cost) for x in range(fighter_arena.width)] for y in range(fighter_arena.height)]
        pathfinder = tcod.path.Pathfinder(tcod.path.SimpleGraph(cost=costs, cardinal=10, diagonal=14))
        pathfinder.add_root(defender.pos)

        lengths: list[tuple[tuple[int, int], int]] = []
        for direction in arena.DIRECTIONS:
            dx, dy = direction
            step = (
                max(0, attacker.pos[0] + dx),
                max(0, attacker.pos[1] + dy),
            )
            lengths.append((direction, len(pathfinder.path_to(step))))
        
        best_path = sorted(lengths, key=lambda length_pair: length_pair[1], reverse=True)[0]
        next_step = best_path[0]
        attacker.move(defender, next_step[0] - attacker.pos[0], next_step[1] - attacker.pos[1])
    except Exception as e:
        print(f"move_away.py: {e}")