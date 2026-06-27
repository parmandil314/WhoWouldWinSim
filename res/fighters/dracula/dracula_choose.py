import fighter
from arena import Arena

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):
    
    self.equipped_weapon = self.weapons["antique sword"]
    if self.in_range(target):
        if self.action_taken:
            return "end_turn"
        elif target.name not in ("Van Helsing", "Dracula", "Frankenstein's Monster"):
            return "bite"
        return "attack"
    return "move"