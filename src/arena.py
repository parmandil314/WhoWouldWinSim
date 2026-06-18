import numpy as np
import tcod


class Tile:
    def __init__(self, name: str, filename: str, char: str, fg: tuple[int, int, int], bg: tuple[int, int, int], walk_cost: float) -> None:
        self.name = name
        self.filename = filename
        self.char = char
        self.fg = fg
        self.bg = bg
        self.walk_cost = walk_cost


class Arena:
    def __init__(self, name: str, width: int, height: int) -> None:

        import load

        self.name = name

        self.a_start: tuple[int, int] = (0, 0)
        self.b_start: tuple[int, int] = (width - 1, height - 1)

        if 4 < width < 20:
            self.width = width
        else:
            self.width = 10
        
        if 4 < height < 20:
            self.height = height
        else:
            self.height = 10
        
        self.tile_types: list[Tile] = load.load_tiles()
        self.tiles = np.zeros(shape=(self.width, self.height), dtype=int)

    
    def draw(self, fighter_a, fighter_b, console: tcod.console.Console):
        console.clear()
        for (x, y), tile in np.ndenumerate(self.tiles):
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


    def is_walkable(self, x, y):
        return self.tile_type(x, y).walk_cost > 0


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
        return (ord(self.tile_types[tile].char), self.tile_types[tile].fg)