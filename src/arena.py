from datetime import datetime

import numpy as np
import tcod


DIRECTIONS = [
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
]


class Message:
    def __init__(self, text: str, fg: tuple[int, int, int] = (255, 255, 255), bg: tuple[int, int, int] = (0, 0, 0)) -> None:
        self.text = text
        self.fg = fg
        self.bg = bg


class Tile:
    def __init__(self, name: str, filename: str, char: str, fg: tuple[int, int, int], bg: tuple[int, int, int], 
                 walk_cost: float, damage: int = 0, is_opaque = False) -> None:
        self.name = name
        self.filename = filename
        self.char = char
        self.fg = fg
        self.bg = bg
        self.walk_cost = walk_cost
        self.is_opaque = is_opaque
        self.damage = damage


class Arena:

    def __init__(self, name: str, folder_path: str, width: int, height: int, editing=False, a_name="a", b_name="b") -> None:

        import load

        self.name = name
        self.folder = folder_path

        self.a_start: tuple[int, int] = (0, 0)
        self.b_start: tuple[int, int] = (width - 1, height - 1)

        if 5 <= width <= 30:
            self.width = width
        else:
            self.width = 10
        
        if 5 <= height <= 30:
            self.height = height
        else:
            self.height = 10

        self.MESSAGE_LOG_MAX_LEN: int = 20
        
        self.tile_types: list[Tile] = load.load_tiles(f"{folder_path.removesuffix("/")}")
        self.tiles = np.zeros(shape=(self.width, self.height), dtype=int)

        self.message_log: list[Message] = []

        if not editing:
            self.tileset = tcod.tileset.load_tilesheet("res/cp437.png", 16, 16, charmap=tcod.tileset.CHARMAP_CP437)
            self.console = tcod.console.Console(80, 50)
            self.context = tcod.context.new(title=f"Who Would Win",
                                        columns=self.console.width, rows=self.console.height, tileset=self.tileset, sdl_window_flags=int(tcod.context.SDL_WINDOW_FULLSCREEN))
            self.file = open(f"transcripts/{a_name} vs. {b_name} in {self.name}: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", "w", encoding="utf-8")
    

    def print(self, text: str, fg: tuple[int, int, int] = (255, 255, 255), bg: tuple[int, int, int] = (0, 0, 0)):
        self.message_log.append(Message(text, fg, bg))
        print(text, file=self.file)
        while len(self.message_log) > self.MESSAGE_LOG_MAX_LEN:
            self.message_log.pop(0)


    def draw_log(self):

        start_x = 1
        start_y = self.height + 1
        i = 0
        for message in self.message_log:
            y = start_y + i
            x = start_x
            self.console.print(x, y, text=message.text, fg=message.fg, bg=message.bg)
            i += 1 + message.text.count("\n")


    def clear(self):
        self.console.clear()

    
    def draw(self, fighter_a, fighter_b):
            
        for (y, x), tile in np.ndenumerate(self.tiles):
            tile_type = self.tile_types[tile]
            self.console.fg[y][x] = tile_type.fg

            color = self.console.bg[y][x]
            if not (color[0] == 0 and color[1] == 255 and color[2] == 0) and not (color[0] == 255 and color[1] == 255 and color[2] == 0):
                self.console.bg[y][x] = tile_type.bg
            self.console.ch[y][x] = ord(tile_type.char)
        
        a_x, a_y = fighter_a.pos
        self.console.fg[a_y][a_x] = (0, 0, 255)
        self.console.ch[a_y][a_x] = ord(fighter_a.char)
        
        b_x, b_y = fighter_b.pos
        self.console.fg[b_y][b_x] = (255, 0, 0)
        self.console.ch[b_y][b_x] = ord(fighter_b.char)
        self.draw_log()
    

    def present(self):
        self.context.present(
            self.console, 
            keep_aspect=True,
            integer_scaling=True,
            align=(0, 0)
        )

    
    def draw_path(self, path: list[tuple[int, int]]):

        for i, point in enumerate(path):
            self.console.bg[point[1]][point[0]] = (0, 255, 0) if i != 0 else (255, 0, 0)


    def is_walkable(self, fighter_a, fighter_b, x, y):

        if not (0 <= x < self.width) or not (0 <= y < self.height):
            return False
        
        if fighter_a.pos == (x, y) or fighter_b.pos == (x, y):
            return False
        
        return self.tile_type(x, y).walk_cost > 0.0


    def is_wall(self, x, y):

        if not (0 <= x < self.width) or not (0 <= y < self.height):
            return False
        
        return self.tile_type(x, y).walk_cost == 0
    

    def tile_type(self, x, y):
        return self.tile_types[self.tiles[y][x]]


    def remove_tile_at(self, x, y):
        self.tiles[y][x] = 0


    def change_tile_at(self, x, y, name):
        for i, tile_type in enumerate(self.tile_types):
            if tile_type.filename == name:
                self.tiles[y][x] = i
                break


    def tile_name_at(self, x, y):
        tile = self.tiles[y][x]
        return self.tile_types[tile].name


    def tile_char_at(self, x, y):
        tile = self.tiles[y][x]
        return (ord(self.tile_types[tile].char), self.tile_types[tile].fg, self.tile_types[tile].bg)

    
    def nearest_wall(self, start_x, start_y):
        costs = [[int(self.tile_type(y, x).walk_cost) for x in range(self.width)] for y in range(self.height)]
        pathfinder = tcod.path.Pathfinder(tcod.path.SimpleGraph(cost=costs, cardinal=10, diagonal=14))
        for y in range(self.height):
            for x in range(self.width):
                if costs[y][x] == 0:
                    pathfinder.add_root((x, y))
        path: list[tuple[int, int]] = pathfinder.path_from((start_x, start_y))[1:].tolist()
        return path
    

    def shortest_path(self, start, end) -> list:
        costs = [[int(self.tile_type(y, x).walk_cost) for x in range(self.width)] for y in range(self.height)]
        pathfinder = tcod.path.Pathfinder(tcod.path.SimpleGraph(cost=costs, cardinal=10, diagonal=14))
        pathfinder.add_root((start[0], start[1]))
        path: np.ndarray = pathfinder.path_to((end[0], end[1]))
        return path[1:].tolist()


    def in_los(self, start: tuple[int, int], end: tuple[int, int]):
        line = tcod.los.bresenham(start, end).tolist()
        for point in line:
            if self.tile_type(*point).is_opaque:
                return False
        return True