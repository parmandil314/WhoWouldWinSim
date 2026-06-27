import fighter
from arena import Arena
import tcod

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):
    
    self.equipped_weapon = self.weapons["scalpel"]
    if not self.action_taken:
        if self.hp > self.max_hp // 2:
            if self.in_range(target):
                self.equipped_weapon = None
                return "attack"
            return "move"
        else:
            if self.in_range(target):
                return "shove"
            elif len(tcod.los.bresenham(self.pos, target.pos)) < 4:
                return "move_away"
            else:
                self.equipped_weapon = self.weapons["revolver"]
                return "attack"
    else:
        if self.hp > self.max_hp // 2:
            return "move"
        else:
            return "move_away"