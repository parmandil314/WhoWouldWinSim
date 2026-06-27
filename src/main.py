import sys

import tcod


class Scene:

    def __init__(self) -> None:

        import load
        import fighter
        
        self.loaded_fighters = load.load_fighters()
        self.valid_fighters = [ fighter for fighter in self.loaded_fighters if fighter.is_character ]

        fighter_a = None
        while fighter_a is None:
            print("Choose your first fighter:")
            for i, f in enumerate(self.valid_fighters):
                print(f"  {i}: {f.name}")
            name = input("> ")
            try:
                fighter_a = self.valid_fighters[int(name)]
                break
            except:
                continue
        self.fighter_a: fighter.Fighter = fighter_a
        
        fighter_b = None
        while fighter_b is None:
            print(f"Choose your second fighter (to fight {self.fighter_a.name}):")
            for i, f in enumerate(self.valid_fighters):
                print(f"  {i}: {f.name}")
            name = input("> ")
            try:
                fighter_b = self.valid_fighters[int(name)]
                break
            except:
                continue
        self.fighter_b: fighter.Fighter = fighter_b

        arena_names: dict = load.load_arena_names()
        arena_names_list = list(arena_names.keys())
        a = None
        while a is None:
            print("Choose the arena in which the battle will occur:")
            for i, name in enumerate(arena_names.keys()):
                print(f"  {i}: {name}")
            name_i = input("> ")
            try:
                a = load.load_arena(arena_names[arena_names_list[int(name_i)]], self.fighter_a.name, self.fighter_b.name)
                break
            except Exception as e:
                print(e)
                continue
        self.fighter_arena = a
        
        self.fighter_a.pos = self.fighter_arena.a_start
        self.fighter_a.arena = self.fighter_arena
        
        self.fighter_b.pos = self.fighter_arena.b_start
        self.fighter_b.arena = self.fighter_arena


    def fight(self):
        
        import arena

        if isinstance(self.fighter_arena, arena.Arena):

            
            self.fighter_arena.console = tcod.console.Console(80, 50)
            

            self.fighter_arena.MESSAGE_LOG_MAX_LEN = self.fighter_arena.console.height - self.fighter_arena.height

            fighting = False
            finished = False
            fighter_a_turn = True
            while True:

                for event in tcod.event.get():
                    if isinstance(event, tcod.event.Quit):
                        raise SystemExit
                    elif isinstance(event, tcod.event.KeyDown):
                        if event.sym.keysym == tcod.event.KeySym.ESCAPE:
                            self.fighter_arena.file.close()
                            self.fighter_arena.context.close()
                            raise SystemExit
                        elif event.sym.keysym == tcod.event.KeySym.SPACE:
                            if not finished:
                                fighting = not fighting

                if fighting:
                    if fighter_a_turn:
                        self.fighter_a.take_turn(self.fighter_b, True)
                    else:
                        self.fighter_b.take_turn(self.fighter_a, False)
                    
                    a_tile = self.fighter_arena.tiles[self.fighter_a.pos[1]][self.fighter_a.pos[0]]
                    b_tile = self.fighter_arena.tiles[self.fighter_b.pos[1]][self.fighter_b.pos[0]]
                    if a_tile == -1:
                        self.fighter_arena.print(f"{self.fighter_a.name} falls to their death!", (255, 0, 0))
                    elif b_tile == -1:
                        self.fighter_arena.print(f"{self.fighter_b.name} falls to their death!", (255, 0, 0))
                    
                    if a_tile == -1 or b_tile == -1 or not self.fighter_a.is_alive or not self.fighter_b.is_alive:
                        fighting = False
                        finished = True
                    
                    fighter_a_turn = not fighter_a_turn
                else:
                    self.fighter_arena.clear()
                    self.fighter_arena.draw(self.fighter_a, self.fighter_b)
                    self.fighter_arena.present()


if __name__ == "__main__":

    scene = Scene()
    scene.fight()