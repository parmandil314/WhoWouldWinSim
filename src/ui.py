import tcod
import pathlib

from map import map_to_json
import arena as arena

def map_rect_clear(map: arena.Arena, start_x: int, start_y: int, dx: int, dy: int):
    
    point_a = (start_x, start_y)
    point_b = (start_x + dx, start_y + dy)

    if point_a == point_b:

        map.remove_tile_at(point_a[0], point_a[1])
    
    elif point_b[0] < point_a[0] and point_a[1] == point_b[1]:

        for x in range(point_b[0], point_a[0]):
            map.remove_tile_at(x, point_a[1])
    
    elif point_b[1] < point_a[1] and point_a[0] == point_b[0]:

        for y in range(point_b[1], point_a[1]):
            map.remove_tile_at(point_a[0], y)

    elif point_b[0] > point_a[0] and point_a[1] == point_b[1]:

        for x in range(point_a[0], point_b[0]):
            map.remove_tile_at(x, point_a[1])
    
    elif point_b[1] > point_a[1] and point_a[0] == point_b[0]:

        for y in range(point_a[1], point_b[1]):
            map.remove_tile_at(point_a[0], y)

    elif point_b[0] < point_a[0] and point_a[1] < point_b[1]:

        for y in range(point_a[1], point_b[1]):
            for x in range(point_b[0], point_a[0]):
                map.remove_tile_at(x, y)
    
    elif point_b[1] < point_a[1] and point_a[0] < point_b[0]:

        for y in range(point_b[1], point_a[1]):
            for x in range(point_a[0], point_b[0]):
                map.remove_tile_at(x, y)

    elif point_b[1] < point_a[1] and point_b[0] < point_a[0]:

        for y in range(point_b[1], point_a[1]):
            for x in range(point_b[0], point_a[0]):
                map.remove_tile_at(x, y)

    else:

        for y in range(point_a[1], point_b[1]):
            for x in range(point_a[0], point_b[0]):
                map.remove_tile_at(x, y)


def load_names_json(path: str) -> list[str]:

    p = pathlib.Path(path)
    file_list = [entry for entry in p.iterdir()]

    return [file.stem for file in file_list if file.name.endswith(".json")]


def new_map(name: str, arena_dir: str, arena_path: str, context: tcod.context.Context, console: tcod.console.Console) -> arena.Arena:

    width = 20
    width_selected = True

    height = 20
    height_selected = False

    def render_dim_selection(context: tcod.context.Context, console: tcod.console.Console, width: int, height: int):

        console.clear()

        console.print(1, 1, "New Map:")
        console.print(5, 5, "Edit map dimensions:")

        if width_selected:
            console.print(5, 8, "WIDTH:  " + str(width), bg=(0, 0, 255))
        else:
            console.print(5, 8, "WIDTH:  " + str(width))
        
        if height_selected:
            console.print(5, 10, "HEIGHT: " + str(height), bg=(0, 0, 255))
        else:   
            console.print(5, 10, "HEIGHT: " + str(height))
        
        context.present(console, keep_aspect=True, integer_scaling=True)

    width_setting = True
    while width_setting:

        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit
            elif isinstance(event, tcod.event.KeyDown):
                if event.sym == tcod.event.KeySym.ESCAPE:
                    raise SystemExit
                elif event.sym == tcod.event.KeySym.RETURN:
                    width_setting = False
                    break
                elif event.sym == tcod.event.KeySym.DOWN or event.sym == tcod.event.KeySym.UP:
                    if width_selected:
                        width_selected = False
                        height_selected = True
                    elif height_selected:
                        width_selected = True
                        height_selected = False
                elif event.sym == tcod.event.KeySym.LEFT:
                    if width_selected:
                        width -= 1
                    elif height_selected:
                        height -= 1
                elif event.sym == tcod.event.KeySym.RIGHT:
                    if width_selected:
                        width += 1
                    elif height_selected:
                        height += 1
            render_dim_selection(context, console, width, height)
    
    def render_terrain_selection(terrain_type: str, context: tcod.context.Context, console: tcod.console.Console, terrain_list: list[str], selected_name: str, set_name: str):

        console.clear()

        console.print(1, 1, "New Map:")
        if terrain_type == "floor":
            console.print(5, 5, "Set map default FLOOR:")
        elif terrain_type == "wall":
            console.print(5, 5, "Set map default WALL:")

        i = 8
        for name in terrain_list:
            if name == set_name and name == selected_name:
                console.print(5, i, "> " + name, bg=(0, 0, 255))
            elif name == selected_name:
                console.print(5, i, "> " + name)
            elif name == set_name:
                console.print(5, i, name, bg=(0, 0, 255))
            else:
                console.print(5, i, name)
            i += 2

        context.present(console, keep_aspect=True, integer_scaling=True) 
    
    terrain_names: list[str] = load_names_json(f"{arena_dir}/tiles")
    
    default_floor: int = 0
    default_wall: int = 0
    for j in range(2):
        i = 0
        selected_index = 0
        terrain_setting = True
        while terrain_setting:
            for event in tcod.event.wait():

                if isinstance(event, tcod.event.Quit):
                    raise SystemExit
                elif isinstance(event, tcod.event.KeyDown):
                    if event.sym == tcod.event.KeySym.ESCAPE:
                        raise SystemExit
                    elif event.sym == tcod.event.KeySym.RETURN:
                        if selected_index == i:
                            terrain_setting = False
                            break
                        else:
                            selected_index = i
                    elif event.sym == tcod.event.KeySym.DOWN:

                        i += 1
                        if i >= len(terrain_names):
                            i = 0
                    
                    elif event.sym == tcod.event.KeySym.UP:
                        
                        i -= 1
                        if i < 0:
                            i = len(terrain_names) - 1
                
                render_terrain_selection("floor" if j == 0 else "wall", context, console, terrain_names, terrain_names[i], terrain_names[selected_index])

        if j == 0:
            default_floor = selected_index
        elif j == 1:
            default_wall = selected_index

    a = arena.Arena(name, arena_dir, width, height)
    for y in range(height):
        for x in range(width):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                a.tiles[y][x] = default_wall
            else:
                a.tiles[y][x] = default_floor
    return a


def render_map(map: arena.Arena, mouse_x: int, mouse_y: int, diff_x: int, diff_y: int, context: tcod.context.Context, console: tcod.console.Console) -> None:
    
    console.clear()
    for y in range(map.height):
        for x in range(map.width):
            terrain_char = map.tile_char_at(x, y)
            console.ch[y][x] = terrain_char[0]
            console.fg[y][x] = terrain_char[1]
            console.bg[y][x] = terrain_char[2]
    
    try:
        console.ch[int(map.a_start[0])][int(map.a_start[1])] = ord("A")
        console.fg[int(map.a_start[0])][int(map.a_start[1])] = (0, 100, 255)
    except:
        pass

    try:
        console.ch[int(map.b_start[0])][int(map.b_start[1])] = ord("B")
        console.fg[int(map.b_start[0])][int(map.b_start[1])] = (255, 0, 0)
    except:
        pass

    point_a = (mouse_x, mouse_y)
    point_b = (mouse_x + diff_x, mouse_y + diff_y)

    if point_a == point_b:

        console.bg[point_a[1]][point_a[0]] = (0, 0, 255)
    
    elif point_b[0] < point_a[0] and point_a[1] == point_b[1]:

        bg_y = point_a[1]
        for bg_x in range(point_b[0], point_a[0]):
            console.bg[bg_y][bg_x] = (0, 0, 255)
    
    elif point_b[1] < point_a[1] and point_a[0] == point_b[0]:

        bg_x = point_a[0]
        for bg_y in range(point_b[1], point_a[1]):
            console.bg[bg_y][bg_x] = (0, 0, 255)

    elif point_b[0] > point_a[0] and point_a[1] == point_b[1]:

        bg_y = point_a[1]
        for bg_x in range(point_a[0], point_b[0]):
            console.bg[bg_y][bg_x] = (0, 0, 255)
    
    elif point_b[1] > point_a[1] and point_a[0] == point_b[0]:

        bg_x = point_a[0]
        for bg_y in range(point_a[1], point_b[1]):
            console.bg[bg_y][bg_x] = (0, 0, 255)

    elif point_b[0] < point_a[0] and point_a[1] < point_b[1]:

        for bg_y in range(point_a[1], point_b[1]):
            for bg_x in range(point_b[0], point_a[0]):
                console.bg[bg_y][bg_x] = (0, 0, 255)
    
    elif point_b[1] < point_a[1] and point_a[0] < point_b[0]:

        for bg_y in range(point_b[1], point_a[1]):
            for bg_x in range(point_a[0], point_b[0]):
                console.bg[bg_y][bg_x] = (0, 0, 255)

    elif point_b[1] < point_a[1] and point_b[0] < point_a[0]:

        for bg_y in range(point_b[1], point_a[1]):
            for bg_x in range(point_b[0], point_a[0]):
                console.bg[bg_y][bg_x] = (0, 0, 255)

    else:

        for bg_y in range(point_a[1], point_b[1]):
            for bg_x in range(point_a[0], point_b[0]):
                console.bg[bg_y][bg_x] = (0, 0, 255)
    
    console.print(map.width + 1, 1, "Tile Contents:")

    terrain_name = map.tile_name_at(mouse_x, mouse_y)
    console.print(map.width + 1, 3, "TERRAIN:")
    console.print(map.width + 2, 4, terrain_name)
    
    context.present(console, keep_aspect=True, integer_scaling=True)


def render_terrain_change_choices(x: int, y: int, terrain_names: list[str], selected_terrain: str, set_terrain: str,
        context: tcod.context.Context, console: tcod.console.Console):

    console.clear()

    console.print(1, 1, "Editing terrain at (" + str(x) + ", " + str(y) + "):")
    console.print(5, 5, "TERRAIN:")

    for i, name in enumerate(terrain_names):
        if name == selected_terrain and name == set_terrain:
            console.print(5, 6 + i, "> " + name, bg=(0, 0, 255))
        elif name == selected_terrain:
            console.print(5, 6 + i, "> " + name)
        elif name == set_terrain:
            console.print(5, 6 + i, name, bg=(0, 0, 255))
        else:
            console.print(5, 6 + i, name)
    
    context.present(console, keep_aspect=True, integer_scaling=True)

def change_terrain_data(
        map: arena.Arena, x: int, y: int, diff_x: int, diff_y: int, terrain_names: list[str], 
        context: tcod.context.Context, console: tcod.console.Console) -> None:

    i = 0
    selected_i = 0
    while True:
        for event in tcod.event.wait():
            if isinstance(event, tcod.event.Quit):
                raise SystemExit
            elif isinstance(event, tcod.event.KeyDown):
                if event.sym.keysym == tcod.event.KeySym.ESCAPE:
                    return
                elif event.sym.keysym == tcod.event.KeySym.RETURN:
                    if i == selected_i:
                        for edit_y in range(y, y + diff_y, 1 if diff_y >= 0 else -1):
                            for edit_x in range(x, x + diff_x, 1 if diff_x >= 0 else -1):
                                map.change_tile_at(edit_x, edit_y, terrain_names[selected_i])
                        return
                    selected_i = i
                elif event.sym.keysym == tcod.event.KeySym.UP:
                    i -= 1
                    if i < 0:
                        i = len(terrain_names) - 1
                elif event.sym.keysym == tcod.event.KeySym.DOWN:
                    i += 1
                    if i >= len(terrain_names):
                        i = 0
            render_terrain_change_choices(x, y, terrain_names, terrain_names[i], terrain_names[selected_i], context, console)

def edit_map_data(map: arena.Arena, context: tcod.context.Context, console: tcod.console.Console):
    
    map_to_edit = map

    mouse_x = 0
    mouse_y = 0
    mouse_diff_x = 1
    mouse_diff_y = 1
    toggle = False

    terrain_names = load_names_json(f"{map.folder}/tiles")

    render_map(map_to_edit, mouse_x, mouse_y, mouse_diff_x, mouse_diff_y, context, console)

    while True:
        context.present(console, keep_aspect=True, integer_scaling=True)
        for e in tcod.event.wait():
            event = context.convert_event(e)
            if isinstance(event, tcod.event.Quit):
                raise SystemExit
            elif isinstance(event, tcod.event.KeyDown):
                if event.sym.keysym == tcod.event.KeySym.ESCAPE:
                    if toggle:
                        toggle = False
                        mouse_diff_x = 1
                        mouse_diff_y = 1
                    else:
                        return None
                elif event.sym.keysym == tcod.event.KeySym.LSHIFT:
                    if not toggle:
                        toggle = True
                    else:
                        toggle = False
                    
                    mouse_diff_x = 1
                    mouse_diff_y = 1
                elif event.sym.keysym == tcod.event.KeySym.BACKSPACE:
                    if toggle:
                        
                        map_rect_clear(map, mouse_x, mouse_y, mouse_diff_x, mouse_diff_y)
                        toggle = False
                        mouse_diff_x = 1
                        mouse_diff_y = 1
                    else:
                        map_to_edit.remove_tile_at(mouse_x, mouse_y)
                elif event.sym.keysym == tcod.event.KeySym.UP:
                    if toggle:
                        if mouse_y + mouse_diff_y - 1 >= 0:
                            mouse_diff_y -= 1
                        if mouse_diff_y == 0:
                            if mouse_y + mouse_diff_y - 1 >= 0:
                                mouse_diff_y -= 1
                    else:
                        if mouse_y - 1 >= 0:
                            mouse_y -= 1
                elif event.sym.keysym == tcod.event.KeySym.DOWN:
                    if toggle:
                        if mouse_y + mouse_diff_y + 1 <= map.height:
                            mouse_diff_y += 1
                        if mouse_diff_y == 0:
                            if mouse_y + mouse_diff_y + 1 <= map.height:
                                mouse_diff_y += 1
                    else:
                        if mouse_y + 1 < map.height:
                            mouse_y += 1
                elif event.sym.keysym == tcod.event.KeySym.LEFT:
                    if toggle:
                        if mouse_x + mouse_diff_x - 1 >= 0:
                            mouse_diff_x -= 1
                        if mouse_diff_x == 0:
                            if mouse_x + mouse_diff_x - 1 >= 0:
                                mouse_diff_x -= 1
                    else:
                        if mouse_x - 1 >= 0:
                            mouse_x -= 1
                elif event.sym.keysym == tcod.event.KeySym.RIGHT:
                    if toggle:
                        if mouse_x + mouse_diff_x + 1 <= map.width:
                            mouse_diff_x += 1
                        if mouse_diff_x == 0:
                            if mouse_x + mouse_diff_x + 1 <= map.width:
                                mouse_diff_x += 1
                    else:
                        if mouse_x + 1 < map_to_edit.width:
                            mouse_x += 1
                elif event.sym.keysym == tcod.event.KeySym.RETURN:
                    change_terrain_data(map_to_edit, mouse_x, mouse_y, mouse_diff_x, mouse_diff_y, terrain_names, context, console)
                    toggle = False
                    mouse_diff_x = 1
                    mouse_diff_y = 1
                elif event.sym.keysym == tcod.event.KeySym.S:
                    save_map_data(map_to_edit)
                elif event.sym.keysym == tcod.event.KeySym.A:
                    map.a_start = (mouse_y, mouse_x)
                elif event.sym.keysym == tcod.event.KeySym.B:
                    map.b_start = (mouse_y, mouse_x)
            render_map(map_to_edit, int(mouse_x), int(mouse_y), mouse_diff_x, mouse_diff_y, context, console)

def save_map_data(map: arena.Arena) -> None:
    with open(f"{map.folder}/{map.name}.json", "w") as file:
        file.write(map_to_json(map))
