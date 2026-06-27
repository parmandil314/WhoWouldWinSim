import fighter
from arena import Arena
import tcod

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):
    
    self.equipped_weapon = self.weapons["scalpel"]
    if not self.action_taken:
        if target.build > 0 and arena.in_los(self.pos, target.pos):
            self.equipped_weapon = self.weapons["revolver"]
            return "attack"
        elif target.build > 0 and arena.distance(self.pos, target.pos) > 6:
            return "move"
        elif self.hp > self.max_hp // 2:
            if self.in_range(target):
                return "attack"
            return "move"
        else:
            if self.in_range(target) and target.build <= 0:
                return "shove"
            elif arena.distance(self.pos, target.pos) < 4:
                return "move_away"
            else:
                self.equipped_weapon = self.weapons["revolver"]
                return "attack"
    else:
        if self.hp > self.max_hp // 2:
            return "move"
        else:
            return "move_away"
