import fighter
from arena import Arena

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    self.equipped_weapon = self.weapons["revolver"]
    if self.in_range(target, self.equipped_weapon.range):
        if self.action_taken:
            return "end_turn"
        return "attack"
    return "move"