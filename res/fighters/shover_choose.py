import fighter
from arena import Arena

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    if not self.in_range(target) and self.tiles_moved <= self.move_rate:
        return "move"
    return "shove"