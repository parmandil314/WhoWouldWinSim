import fighter
from arena import Arena
import tcod

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter):
    
    try:
        if attacker.tiles_moved + 1 <= attacker.move_rate:
        
            costs = [[int(arena.tile_type(x, y).walk_cost) for x in range(arena.width)] for y in range(arena.height)]
            pathfinder = tcod.path.Pathfinder(tcod.path.SimpleGraph(cost=costs, cardinal=2, diagonal=3))
            pathfinder.add_root(defender.pos)

            DIRECTIONS = [
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
                (0, -1),
                (0, 1),
                (-1, 0),
                (1, 0),
            ]

            lengths: list[tuple[tuple[int, int], int]] = []
            for direction in DIRECTIONS:
                lengths.append((direction, len(pathfinder.path_to((attacker.pos[0] + direction[0], attacker.pos[1] + direction[1])))))
            
            best_path = sorted(lengths, key=lambda length_pair: length_pair[1], reverse=True)[0]
            next_step = best_path[0]
            if arena.is_walkable(attacker, defender, next_step[0], next_step[1]):
                attacker.move(defender, next_step[1] - attacker.pos[1], next_step[0] - attacker.pos[0])
                attacker.tiles_moved += 1
    except Exception as e:
        print(e)