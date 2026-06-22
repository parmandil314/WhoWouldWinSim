import fighter
from arena import Arena

import tcod

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    if not self.in_range(target) and self.tiles_moved > 0:
        return "move"
    return "punch"