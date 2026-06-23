import copy
import time
import tcod


def default_choose_ability(arena, attacker, target) -> str:
    return "none"


class Fighter:

    ENERGY_THRESHOLD = 5

    def __init__(self, name: str, is_character: bool):

        from arena import Arena

        self.name = name
        self.char = name[0]
        self.is_character = is_character

        self.pos: tuple[int, int] = (0, 0)

        self.hp = 10
        self.max_hp = 10
        self.is_alive = True

        self.db = 0
        self.armor = 0 # damage -= armor

        self.abilities = {}
        self.choose_ability = default_choose_ability
        self.skills: dict[str, int] = {}
        self.attributes: dict[str, int] = {}

        self.dodge: str = "defender.hp < 50"

        self.move_rate = 1
        self.tiles_moved = 0
        self.action_taken = False

        self.arena: Arena


    def take_damage(self, damage: int, print_effects=True):

        mod_damage = damage - self.armor
        self.hp -= mod_damage
        if print_effects:
            self.arena.print(f"{self.name} takes {mod_damage} damage!")

        if self.hp > 0:
            if self.hp < self.max_hp // 2:
                self.arena.print(f"{self.name} looks unsteady!")
            elif self.hp < self.max_hp // 4:
                self.arena.print(f"{self.name} looks desperate!")
        else:
            self.is_alive = False
            self.arena.print(f"{self.name} loses!")
    

    def move(self, other, dx, dy):

        mod_dx = int(dx)
        if dx > 1:
            mod_dx = 1
        elif dx < -1:
            mod_dx = -1
        
        mod_dy = int(dy)
        if dy > 1:
            mod_dy = 1
        elif dy < -1:
            mod_dy = -1

        new_pos = (self.pos[0] + mod_dx, self.pos[1] + mod_dy)
        if self.arena.is_walkable(self, other, *new_pos):
            self.pos = new_pos
            self.tiles_moved += 1

    
    def in_range(self, other, range=0):
        distance = len(tcod.los.bresenham(self.pos, other.pos))
        if distance <= 2 + range:
            return True
        return False


    def take_turn(self, scene, arena, context, console, opponent):

        self.action_taken = False
        self.tiles_moved = 0
        for _ in range(self.move_rate):
            scene.draw(context, console)
            time.sleep(0.2)
            self.use_ability(arena, self.choose_ability(arena, self, opponent), opponent)


    def use_ability(self, arena, name: str, target):

        try:
            self.abilities[name](arena, self, target)
        except Exception as e:
            print(e)