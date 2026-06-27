from pathlib import Path

import numpy as np

import json

import arena as arena

def map_terrain_to_json(processed_map: arena.Arena) -> str:
    string = '"tiles": ['

    for tile in processed_map.tiles.flatten():
        string += f"{str(tile)},"
    
    string = string.removesuffix(",")
    string += "]"

    return string

def map_to_json(processed_map: arena.Arena) -> str:
    string = '{\n"name" : "' + processed_map.name + '",\n"width" : ' + str(processed_map.width) + ',\n"height" : ' + str(processed_map.height) + ',\n"a_start" : ' + str(list(processed_map.a_start)) + ',\n"b_start" : ' + str(list(processed_map.b_start)) + ','
    string += "\n" + map_terrain_to_json(processed_map)
    string += "\n}"

    return string

def load_map_data(path: str) -> arena.Arena:

    json_data: dict = {}
    with open(path, "r") as file:
        json_data = json.loads(file.read())
    
    data = arena.Arena(json_data["name"], str(Path(path).parent), json_data["width"], json_data["height"], True)

    data.a_start = tuple(json_data["a_start"])
    data.b_start = tuple(json_data["b_start"])
    
    json_tiles = list(json_data["tiles"])
    tiles = np.reshape(json_tiles, (data.width, data.height))
    data.tiles = tiles
    
    return data