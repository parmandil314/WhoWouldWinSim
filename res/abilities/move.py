import fighter
from arena import Arena
import dice
import tcod
import numpy

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter) -> int:
    
    try:
        costs = [[int(arena.tile_type(x, y).walk_cost) for x in range(arena.width)] for y in range(arena.height)]
        path: numpy.ndarray = tcod.path.path2d(costs, start_points=[attacker.pos], end_points=[defender.pos], cardinal=2, diagonal=3)
        next_step: tuple[int, int] = (path[1][0], path[1][1])
        if arena.is_walkable(attacker, defender, next_step[0], next_step[1]):
            attacker.move(next_step[0] - attacker.pos[0], next_step[1] - attacker.pos[1])
    except Exception as e:
        print(e)
    return 0