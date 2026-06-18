import numpy as np
import tcod

import load


class Tile:
    def __init__(self, name: str, char: str, fg: tuple[int, int, int], bg: tuple[int, int, int], walk_cost: float) -> None:
        self.name = name
        self.char = char
        self.fg = fg
        self.bg = bg
        self.walk_cost = walk_cost


class Arena:
    def __init__(self, name: str, width: int, height: int) -> None:

        self.name = name

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
        
        console.fg[fighter_a.y][fighter_a.x] = (0, 0, 255)
        console.ch[fighter_a.y][fighter_a.x] = ord(fighter_a.char)
        
        console.fg[fighter_b.y][fighter_b.x] = (0, 0, 0)
        console.ch[fighter_b.y][fighter_b.x] = ord(fighter_b.char)
