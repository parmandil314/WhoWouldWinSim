from pathlib import Path
import sys
import tcod

from map import load_map_data
from ui import new_map, edit_map_data, save_map_data

def names_at(dir_path: str) -> dict[str, str]:

    path = Path(dir_path)

    maps: dict[str, str] = {}
    for folder in path.iterdir():
        if folder.is_dir():
            for file in folder.iterdir():
                if file.is_file() and file.name.endswith(".json"):
                    maps[file.name.removesuffix(".json")] = str(file.resolve())
    return maps

maps: dict[str, str] = names_at("res/arenas")

tileset = tcod.tileset.load_tilesheet(
    "res/cp437.png", columns=16, rows=16, charmap=tcod.tileset.CHARMAP_CP437
)

map_data = None
if sys.argv[1] not in maps.keys():
    console = tcod.console.Console(80, 50)
    context = tcod.context.new(title="Map Editor", console=console, tileset=tileset, sdl_window_flags=int(tcod.context.SDL_WINDOW_FULLSCREEN))
    map_data = new_map(sys.argv[1], context, console)
    console = tcod.console.Console(map_data.width + 30, map_data.height)
    
    map_data = edit_map_data(map_data, context, console)

    context.close()
else:
    map_data = load_map_data(maps[sys.argv[1]])
    console = tcod.console.Console(map_data.width + 30, map_data.height)
    context = tcod.context.new(title="Map Editor", console=console, tileset=tileset, sdl_window_flags=int(tcod.context.SDL_WINDOW_FULLSCREEN))
    
    map_data = edit_map_data(map_data, context, console)
    
    context.close()

if not map_data is None:
    save_map_data(map_data)