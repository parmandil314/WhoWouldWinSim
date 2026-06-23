import fighter
from arena import Arena

import tcod

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    state = "normal"
    if self.hp < self.max_hp / 2:
        state = "careful"

    match state:
        case "normal":
            if not self.in_range(target):
                return "move"
            return "punch"
        case "careful":
            if self.in_range(target) and self.tiles_moved == self.move_rate - 1:
                return "move_away"
            elif self.in_range(target) and self.tiles_moved < self.move_rate - 1:
                return "punch"
            else:
                return "move"