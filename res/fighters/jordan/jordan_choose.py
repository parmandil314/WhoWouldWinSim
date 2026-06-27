import fighter
from arena import Arena

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):
    
    self.equipped_weapon = self.weapons["golf club"]
    if self.in_range(target):
        if self.action_taken:
            return "end_turn"
        return "attack"
    return "move"