import copy
import sys

import arena, load

fighters = load.load_fighters()

arena_paths = load.load_arena_names().values()

for i in range(int(sys.argv[1])):
    for a in range(len(fighters)):
        for b in range(len(fighters)):

            if a == b:
                continue
            
            for arena_path in arena_paths:

                fighter_a = copy.deepcopy(fighters[a])
                fighter_b = copy.deepcopy(fighters[b])
                
                arena = load.load_arena(arena_path, fighter_a.name, fighter_b.name, True)

                fighter_a.pos = arena.a_start
                fighter_a.arena = arena
                
                fighter_b.pos = arena.b_start
                fighter_b.arena = arena

                a_turn = True
                while True:
                    if a_turn:
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
                        break
                    
                    a_turn = not a_turn

                with open(f"fight_data/{fighter_a.name}:{fighter_b.name}:{arena.name}:{i}", "w", encoding="utf-8") as f:
                    text = "{" + '"a_hp": ' + str(fighter_a.hp) + ', "b_hp": ' + str(fighter_b.hp) + "}"
                    print(text, file=f)
