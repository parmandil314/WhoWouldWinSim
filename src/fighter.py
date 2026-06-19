import copy


class Limb:
    def __init__(self, name: str, max_hp: int):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp


def default_choose_ability(attacker, target) -> str:
    return "none"


class Fighter:

    ENERGY_THRESHOLD = 5

    def __init__(self, name: str, is_character: bool):

        self.name = name
        self.char = name[0]
        self.is_character = is_character

        self.pos: tuple[int, int] = (0, 0)

        self.hp = 100
        self.max_hp = 100
        self.is_alive = True

        self.armor = 1.0 # multiplied by damage; 1.0 is no armor and 0.0 is impenetrable armor
        # self.limbs: list[Limb] = []
        self.abilities = {}
        self.choose_ability = default_choose_ability
        self.skills: dict[str, int] = {}
        self.attributes: dict[str, int] = {}
        self.dodge_if: str = "defender.hp < 50"

        self.energy: int = 5
        self.speed: int = 3
        self.move_speed = 1.0


    def take_damage(self, damage: int, print_effects=True):
        modified_damage = damage * self.armor
        self.hp -= modified_damage
        if print_effects:
            print(f"{self.name} takes {damage} damage!")

        if self.hp > 0:
            if self.hp < self.max_hp // 2:
                print(f"{self.name} looks unsteady!")
            elif self.hp < self.max_hp // 4:
                print(f"{self.name} looks desperate!")
        else:
            self.is_alive = False
            print(f"{self.name} loses!")
    

    def move(self, dx, dy):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)


    def regain_energy(self):
        self.energy += self.speed


def attacker_take_turn(arena, attacker, opponent):

    attacker_use_ability(arena, attacker, attacker.choose_ability(arena, attacker, opponent), opponent)


def attacker_use_ability(arena, attacker, name: str, target):

    try:
        attacker.energy -= attacker.abilities[name](arena, attacker, target)
    except Exception as e:
        print(f"{e}")