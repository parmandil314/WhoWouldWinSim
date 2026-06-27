import fighter
from arena import Arena

def execute(arena: Arena, attacker: fighter.Fighter, defender: fighter.Fighter):

    try:
        path = arena.shortest_path(attacker.pos, defender.pos)
        arena.draw_path(path)
        next_step: tuple[int, int] = path[0]
        attacker.move(defender, next_step[0] - attacker.pos[0], next_step[1] - attacker.pos[1])
    except Exception as e:
        print(f"move.py: {e}")