import copy
import sys
from itertools import combinations, product
import traceback

import arena, load

fighters = load.load_fighters()
arena_paths = list(load.load_arena_names().values())
pairs = combinations(fighters, 2)
matches = [(*pair, path) for pair, path in product(pairs, arena_paths)]

for i in range(int(sys.argv[1])):

    for (a, b, arena_path) in matches:

        try:
            fighter_a = copy.deepcopy(a)
            fighter_b = copy.deepcopy(b)
            
            arena = load.load_arena(arena_path, fighter_a.name, fighter_b.name, True)

            fighter_a.pos = arena.a_start
            fighter_a.arena = arena
            
            fighter_b.pos = arena.b_start
            fighter_b.arena = arena

            a_turn = True
            fighting = True
            while fighting:
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
                
                fighting = a_tile != -1 and b_tile != -1 and fighter_a.is_alive and fighter_b.is_alive
                
                a_turn = not a_turn

            with open(f"fight_data/{fighter_a.name}:{fighter_b.name}:{arena.name}:{i}", "w", encoding="utf-8") as f:
                text = "{" + '"a_hp": ' + str(fighter_a.hp) + ', "b_hp": ' + str(fighter_b.hp) + "}"
                print(text, file=f)
        except:
            print(f"batch_sim: {a.name} vs. {b.name}")
            traceback.print_exc()
            raise SystemExit
