import fighter
from arena import Arena

def choose_ability(arena: Arena, self: fighter.Fighter, target: fighter.Fighter):

    careful = self.hp < self.max_hp // 2

    if not self.action_taken:
        if not careful:
            if self.in_range(target):
                return "attack"
        elif careful and self.tiles_moved > self.move_rate:
            return "end_turn"
        
    if not careful:
        return "move"
    return "move_away"