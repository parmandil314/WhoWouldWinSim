import arena, load

fighters = [ fighter for fighter in load.load_fighters() if fighter.is_character ]
arena_names = load.load_arena_names()

for fighter_a in fighters:
    for fighter_b in fighters:

        if fighter_a == fighter_b:
                continue
        
        for arena_name in arena_names.values():

            arena = load.load_arena(arena_name, fighter_a.name, fighter_b.name, True)

            fighter_a.pos = arena.a_start
            fighter_a.arena = arena
            
            fighter_b.pos = arena.b_start
            fighter_b.arena = arena

            fighter_a_turn = True
            while True:
                if fighter_a_turn:
                    fighter_a.take_turn(fighter_b, True)
                else:
                    fighter_b.take_turn(fighter_a, False)
                
                a_tile = arena.tiles[fighter_a.pos[1]][fighter_a.pos[0]]
                b_tile = arena.tiles[fighter_b.pos[1]][fighter_b.pos[0]]
                if a_tile == -1:
                    arena.print(f"{fighter_a.name} falls to their death!", (255, 0, 0))
                elif b_tile == -1:
                    arena.print(f"{fighter_b.name} falls to their death!", (255, 0, 0))
                
                if a_tile == -1 or b_tile == -1 or not fighter_a.is_alive or not fighter_b.is_alive:
                    fighting = False
                    break
                
                fighter_a_turn = not fighter_a_turn