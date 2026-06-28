import fighter
from arena import Arena

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):
    
    if not self.action_taken:
        if self.in_range(target):
            if target.name in ("Van Helsing", "Dracula", "Frankenstein's Monster"):
                self.equipped_weapon = self.weapons["antique sword"]
                return "attack"
            return "bite"
    return "move"