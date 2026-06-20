import copy
import tcod


def default_choose_ability(attacker, target) -> str:
    return "none"


class Fighter:

    ENERGY_THRESHOLD = 5

    def __init__(self, name: str, is_character: bool):

        from arena import Arena

        self.name = name
        self.char = name[0]
        self.is_character = is_character

        self.pos: tuple[int, int] = (0, 0)

        self.hp = 100
        self.max_hp = 100
        self.is_alive = True

        self.db = 0
        self.armor = 1 # damage -= armor

        self.abilities = {}
        self.choose_ability = default_choose_ability
        self.skills: dict[str, int] = {}
        self.attributes: dict[str, int] = {}

        self.dodge_if: str = "defender.hp < 50"

        self.energy: int = Fighter.ENERGY_THRESHOLD
        self.speed: int = 3
        self.move_speed = 1.0
        self.move_rate = 8 # MOV
        self.tiles_moved = 0

        self.arena: Arena


    def take_damage(self, damage: int, print_effects=True):
        self.hp -= damage
        if print_effects:
            self.arena.print(f"{self.name} takes {damage} damage!")

        if self.hp > 0:
            if self.hp < self.max_hp // 2:
                self.arena.print(f"{self.name} looks unsteady!")
            elif self.hp < self.max_hp // 4:
                self.arena.print(f"{self.name} looks desperate!")
        else:
            self.is_alive = False
            self.arena.print(f"{self.name} loses!")
    

    def move(self, dx, dy):
        pos = (self.pos[0] + dx, self.pos[1] + dy)
        
        num_tiles = len(tcod.los.bresenham(self.pos, pos))

        if self.tiles_moved - num_tiles >= 0:
            self.tiles_moved -= num_tiles
            self.pos = pos


    def regain_energy(self):
        self.energy += self.speed


def attacker_take_turn(arena, attacker, opponent):

    attacker_use_ability(arena, attacker, attacker.choose_ability(arena, attacker, opponent), opponent)


def attacker_use_ability(arena, attacker, name: str, target):

    try:
        energy_used = attacker.abilities[name](arena, attacker, target)
        attacker.energy -= energy_used
    except Exception as e:
        print(e)