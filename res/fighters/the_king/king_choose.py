import fighter
from arena import Arena


def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    if not self.action_taken:
        self.equipped_weapon = self.weapons["knife"]
        return "attack"
    
    if self.hp < self.max_hp // 2:
        return "move_away"
    return "move"
