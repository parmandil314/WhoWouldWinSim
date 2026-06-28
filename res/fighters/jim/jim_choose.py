import fighter
from arena import Arena
import tcod


def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    if not self.action_taken:
        if self.in_range(target):
            if self.hp > self.max_hp // 2:
                return "attack"
            else:
                return "shove"
    else:
        if self.hp > self.max_hp // 2:
            return "move"
        else:
            return "move_away"
    return "move"