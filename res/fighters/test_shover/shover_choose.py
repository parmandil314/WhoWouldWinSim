import fighter
from arena import Arena

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    if self.in_range(target):
        if self.action_taken:
            return "end_turn"
        return "shove"
    return "move"