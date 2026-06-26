import fighter
from arena import Arena
import tcod
import numpy

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter):
    
    try:
        if attacker.tiles_moved + 1 <= attacker.move_rate:
            path = arena.shortest_path(attacker.pos, defender.pos)
            next_step: tuple[int, int] = (path[1][0], path[1][1])
            attacker.move(defender, next_step[0] - attacker.pos[0], next_step[1] - attacker.pos[1])
    except Exception as e:
        print(e)