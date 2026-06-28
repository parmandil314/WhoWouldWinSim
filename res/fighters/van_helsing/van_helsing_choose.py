import fighter
from arena import Arena
import tcod


def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    if target.name == "Dracula":
        if not self.action_taken:
            if self.hp > self.max_hp // 2:
                if self.in_range(target, 1):
                    return "holy_water"
                return "move"
            else:
                if arena.in_los(self.pos, target.pos) and self.in_range(target, 5):
                    return "crucifix"
                else:
                    return "move"
        else:
            if self.hp > self.max_hp // 2:
                return "move"
            else:
                return "move_away"

    else:
        if self.action_taken:
            if self.hp > self.max_hp // 2:
                return "move"
            else:
                return "move_away"
        else:
            if self.hp > self.max_hp // 2 and target.build <= 0:
                if self.in_range(target):
                    self.equipped_weapon = self.weapons["knife"]
                    return "attack"
                return "move"
            else:
                if self.in_range(target):
                    return "shove"
                elif arena.distance(self.pos, target.pos) < 4:
                    return "move_away"
                else:
                    self.equipped_weapon = self.weapons["revolver"]
                    return "attack"