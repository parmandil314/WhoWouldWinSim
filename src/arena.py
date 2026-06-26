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
    def __init__(self, name: str, filename: str, char: str, fg: tuple[int, int, int], bg: tuple[int, int, int], walk_cost: float, damage: int = 0) -> None:
        self.name = name
        self.filename = filename
        self.char = char
        self.fg = fg
        self.bg = bg
        self.walk_cost = walk_cost
        self.damage = damage


class Arena:

    def __init__(self, name: str, folder_path: str, width: int, height: int) -> None:

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

    
    def print(self, text: str, fg: tuple[int, int, int] = (255, 255, 255), bg: tuple[int, int, int] = (0, 0, 0)):
        self.message_log.append(Message(text, fg, bg))
        while len(self.message_log) > self.MESSAGE_LOG_MAX_LEN:
            self.message_log.pop(0)


    def draw_log(self, console: tcod.console.Console):

        start_x = 1
        start_y = self.height + 1
        i = 0
        for message in self.message_log:
            y = start_y + i
            x = start_x
            console.print(x, y, text=message.text, fg=message.fg, bg=message.bg)
            i += 1 + message.text.count("\n")

    
    def draw(self, fighter_a, fighter_b, console: tcod.console.Console):
        console.clear()
        for (y, x), tile in np.ndenumerate(self.tiles):
            tile_type = self.tile_types[tile]
            console.fg[y][x] = tile_type.fg
            console.bg[y][x] = tile_type.bg
            console.ch[y][x] = ord(tile_type.char)
        
        a_x, a_y = fighter_a.pos
        console.fg[a_y][a_x] = (0, 0, 255)
        console.ch[a_y][a_x] = ord(fighter_a.char)
        
        b_x, b_y = fighter_b.pos
        console.fg[b_y][b_x] = (255, 0, 0)
        console.ch[b_y][b_x] = ord(fighter_b.char)
        self.draw_log(console)


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
        costs = [[int(self.tile_type(x, y).walk_cost) for x in range(self.width)] for y in range(self.height)]
        pathfinder = tcod.path.Pathfinder(tcod.path.SimpleGraph(cost=costs, cardinal=2, diagonal=3))
        for y in range(self.height):
            for x in range(self.width):
                if costs[y][x] == 0:
                    pathfinder.add_root((y, x))
        path: list[tuple[int, int]] = pathfinder.path_from((start_x, start_y))[1:].tolist()
        return path
    

    def shortest_path(self, start, end, points_to_avoid: list[tuple[int, int]] = []) -> list:
        costs = [[int(self.tile_type(x, y).walk_cost) for x in range(self.width)] for y in range(self.height)]
        for point in points_to_avoid:
            x, y = point
            costs[y][x] = 0
        pathfinder = tcod.path.Pathfinder(tcod.path.SimpleGraph(cost=costs, cardinal=2, diagonal=3))
        pathfinder.add_root(start)
        path: np.ndarray = pathfinder.path_to(end)
        return path.tolist()