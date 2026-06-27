import fighter
from arena import Arena
import tcod


def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    if not self.action_taken:
        if self.hp > self.max_hp * 0.75:
            if self.in_range(target):
                self.equipped_weapon = None
                return "attack"
            return "move"
        else:
            if self.in_range(target):
                return "shove"
            elif arena.distance(self.pos, target.pos) < 6:
                return "move_away"
            else:
                self.equipped_weapon = self.weapons["revolver"]
                return "attack"
    else:
        if self.hp > self.max_hp * 0.75:
            return "move"
        else:
            return "move_away"
