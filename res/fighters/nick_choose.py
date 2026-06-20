import fighter
from arena import Arena

import tcod

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    if len(tcod.los.bresenham(self.pos, target.pos)) > 2 and self.tiles_moved > 0:
        return "move"
    return "punch"