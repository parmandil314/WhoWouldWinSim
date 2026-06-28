import fighter
from arena import Arena
import tcod

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):
    
    self.equipped_weapon = self.weapons["scalpel"]
    if not self.action_taken:
        if arena.in_los(self.pos, target.pos):
            self.equipped_weapon = self.weapons["revolver"]
            return "attack"
        elif self.in_range(target):
            return "move_away"
    return "move"