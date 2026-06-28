import fighter
from arena import Arena
import traceback

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter):

    try:
        path = arena.shortest_path(attacker.pos, defender.pos)
        if len(path) == 0:
            return
        # arena.draw_path(path)
        next_step: tuple[int, int] = path[-2]
        attacker.pos = next_step
    except Exception as e:
        print(f"{attacker.name}: move.py: {e}")
        traceback.print_exc()