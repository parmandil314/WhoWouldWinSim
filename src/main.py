import tcod
import time


class Scene:

    import arena
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
                a = load.load_arena(arena_names[arena_names_list[int(name_i)]])
                break
            except:
                continue
        self.fighter_arena = a
        
        self.fighter_a.pos = self.fighter_arena.a_start
        self.fighter_b.pos = self.fighter_arena.b_start
    

    def draw(self, context: tcod.context.Context, console: tcod.console.Console):
        self.fighter_arena.draw(self.fighter_a, self.fighter_b, console)
        context.present(
            console, 
            keep_aspect=True,
            integer_scaling=True,
            align=(0, 0)
        )

        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit


    def fight(self):
        
        import arena

        if isinstance(self.fighter_arena, arena.Arena):

            tileset = tcod.tileset.load_tilesheet("res/cp437.png", 16, 16, charmap=tcod.tileset.CHARMAP_CP437)
            console = tcod.console.Console(80, 50)
            context = tcod.context.new(title=f"Who Would Win: {self.fighter_a.name} vs. {self.fighter_b.name}",
                                       columns=console.width, rows=console.height, tileset=tileset, sdl_window_flags=int(tcod.context.SDL_WINDOW_FULLSCREEN))
        
            import fighter

            while self.fighter_a.is_alive and self.fighter_b.is_alive:

                a_turn = True
                while a_turn:
                    self.draw(context, console)
                    fighter.attacker_take_turn(self.fighter_arena, self.fighter_a, self.fighter_b)
                    self.fighter_b.regain_energy()
                    a_turn = self.fighter_a.energy > 0
                    time.sleep(0.25)
                
                b_turn = True
                while b_turn:
                    self.draw(context, console)
                    fighter.attacker_take_turn(self.fighter_arena, self.fighter_b, self.fighter_a)
                    self.fighter_a.regain_energy()
                    b_turn = self.fighter_b.energy > 0
                    time.sleep(0.25)


if __name__ == "__main__":
    scene = Scene()
    scene.fight()