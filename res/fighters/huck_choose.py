import fighter
from arena import Arena

import tcod

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    state = "normal"
    if self.hp < self.max_hp - 40:
        state = "careful"

    match state:
        case "normal":
            if len(tcod.los.bresenham(self.pos, target.pos)) > 2:
                return "move"
            return "punch"
        case "careful":
            if self.energy < 3:
                return "move_away"
            elif self.energy == fighter.Fighter.ENERGY_THRESHOLD:
                return "move"
            else:
                return "punch"