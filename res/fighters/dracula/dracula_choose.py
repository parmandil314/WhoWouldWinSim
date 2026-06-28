import fighter
from arena import Arena

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):
    
    self.equipped_weapon = self.weapons["antique sword"]
    if not self.action_taken:
        if target.name not in ("Van Helsing", "Dracula", "Frankenstein's Monster"):
            return "bite"
        elif self.in_range(target):
            return "attack"
    return "move"