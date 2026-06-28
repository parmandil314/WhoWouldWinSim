import fighter
from arena import Arena
import tcod


def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    if target.name == "Dracula":
        if not self.action_taken:
            if self.in_range(target, 1):
                return "holy_water"
            if arena.in_los(self.pos, target.pos) and self.in_range(target, 5):
                return "crucifix"
        else:
            if self.in_range(target):
                return "move_away"
            else:
                return "move"

    elif not self.action_taken:
        if arena.in_los(self.pos, target.pos) and self.in_range(target, 15):
            self.equipped_weapon = self.weapons["revolver"]
            return "attack"
        elif self.in_range(target):
            self.equipped_weapon = None
            return "attack"
    return "move"