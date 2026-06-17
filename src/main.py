#!/usr/bin/python3


class Scene:

    def __init__(self) -> None:

        import load
        
        self.loaded_fighters = load.load_fighters()
        self.valid_fighters = [ fighter for fighter in self.loaded_fighters if fighter.is_character ]

        fighter_a = None
        while fighter_a is None:
            print("Choose your first fighter:")
            for i, fighter in enumerate(self.valid_fighters):
                print(f"  {i}: {fighter.name}")
            name = input("> ")
            try:
                fighter_a = self.valid_fighters[int(name)]
                break
            except:
                continue
        self.fighter_a = fighter_a
        
        fighter_b = None
        while fighter_b is None:
            print(f"Choose your second fighter (to fight {fighter_a.name}):")
            for i, fighter in enumerate(self.valid_fighters):
                print(f"  {i}: {fighter.name}")
            name = input("> ")
            try:
                fighter_b = self.valid_fighters[int(name)]
                break
            except:
                continue
        self.fighter_b = fighter_b
        
    
    def fight(self):

        import fighter

        a_turn = True
        while self.fighter_a.is_alive and self.fighter_b.is_alive:
            if a_turn:
                fighter.attacker_take_turn(self.fighter_a, self.fighter_b)
            else:
                fighter.attacker_take_turn(self.fighter_b, self.fighter_a)
            a_turn = not a_turn


if __name__ == "__main__":
    scene = Scene()
    scene.fight()