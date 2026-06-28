import fighter
from arena import Arena

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):
    
    self.equipped_weapon = self.weapons["antique sword"]
    if not self.action_taken:
        if self.in_range(target):
            if target.name not in ("Van Helsing", "Dracula", "Frankenstein's Monster"):
                return "bite"
            return "attack"
    return "move"