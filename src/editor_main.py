from pathlib import Path
import sys
import tcod

from map import load_map_data
from ui import new_map, edit_map_data, save_map_data

def names_at(dir_path: str) -> list[str]:

    path = Path(dir_path)
    return [file.stem for file in path.iterdir() if file.is_file()]

map_names = names_at("res/arenas")

tileset = tcod.tileset.load_tilesheet(
    "res/cp437.png", columns=16, rows=16, charmap=tcod.tileset.CHARMAP_CP437
)

map_data = None
if sys.argv[1] not in map_names:
    console = tcod.console.Console(80, 50)
    context = tcod.context.new(title="Map Editor", console=console, tileset=tileset, sdl_window_flags=int(tcod.context.SDL_WINDOW_FULLSCREEN))
    map_data = new_map(sys.argv[1], context, console)
    console = tcod.console.Console(map_data.width + 30, map_data.height)
    
    map_data = edit_map_data(map_data, context, console)

    context.close()
else:
    map_data = load_map_data("res/arenas/" + sys.argv[1] + ".json")
    console = tcod.console.Console(map_data.width + 30, map_data.height)
    context = tcod.context.new(title="Map Editor", console=console, tileset=tileset, sdl_window_flags=int(tcod.context.SDL_WINDOW_FULLSCREEN))
    
    map_data = edit_map_data(map_data, context, console)
    
    context.close()

if not map_data is None:
    save_map_data(map_data)