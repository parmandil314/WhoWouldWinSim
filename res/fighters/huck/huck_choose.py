import fighter
from arena import Arena

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    state = "normal"
    if self.hp < self.max_hp / 2:
        state = "careful"

    if state == "normal":
        if not self.in_range(target):
            return "move"
        return "attack"
    elif state == "careful":
        if self.in_range(target) and self.tiles_moved == self.move_rate - 1:
            return "move_away"
        elif self.in_range(target) and self.tiles_moved < self.move_rate - 1:
            return "attack"
        else:
            return "move"
    return "move"