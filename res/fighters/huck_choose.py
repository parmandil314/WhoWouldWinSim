import fighter
from arena import Arena

import tcod

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    state = "normal"
    if self.hp < self.max_hp / 2:
        state = "careful"

    match state:
        case "normal":
            if len(tcod.los.bresenham(self.pos, target.pos)) > 2 and self.tiles_moved > 0:
                return "move"
            return "punch"
        case "careful":
            if self.tiles_moved > 4:
                return "move_away"
            elif len(tcod.los.bresenham(self.pos, target.pos)) > 2 and self.tiles_moved <= 4:
                return "move"
            else:
                return "punch"