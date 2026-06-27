import time
import tcod
import dice


def default_choose_ability(arena, attacker, target) -> str:
    return "none"


class Weapon:
    def __init__(self, name: str, skill: str, num_attacks: int, weapon_range: int, num_dice: int, dice_sides: int, modifier: int = 0) -> None:
        self.name = name
        self.skill = skill
        self.num_attacks = num_attacks
        self.range = weapon_range
        self.num_dice = num_dice
        self.dice_sides = dice_sides
        self.modifier = modifier
    

    def roll_damage(self):
        return dice.roll(self.num_dice, self.dice_sides, self.modifier)


DEFAULT_MELEE_WEAPON = Weapon("Fists", "brawl", 1, 0, 1, 3)


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

        self.build = 0
        self.db = 0
        self.armor = 0 # damage -= armor

        self.weapons: dict[str, Weapon] = {}
        self.equipped_weapon: None | Weapon = None

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
            self.arena.print(f"{self.name} takes {mod_damage} damage!", (255, 0, 0))

        if self.hp > 0:
            if self.hp < self.max_hp // 2:
                self.arena.print(f"{self.name} looks unsteady!", (255, 255, 0))
            elif self.hp < self.max_hp // 4:
                self.arena.print(f"{self.name} looks desperate!", (255, 0, 0))
        else:
            self.is_alive = False
            self.arena.print(f"{self.name} loses!", (255, 0, 0))
    

    def move(self, other, dx, dy):

        if self.tiles_moved > self.move_rate:
            return

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

    
    def in_range(self, other, range=0):
        distance = len(tcod.los.bresenham(self.pos, other.pos))
        if distance <= 2 + range:
            return True
        return False


    def take_turn(self, scene, context, console, opponent, a):

        self.action_taken = False
        self.tiles_moved = 0
        while self.tiles_moved <= self.move_rate:
            self.arena.clear()
            if a:
                self.arena.draw(self, opponent)
            else:
                self.arena.draw(opponent, self)
            time.sleep(0.15)
            ability_choice = self.choose_ability(self.arena, self, opponent)
            if ability_choice == "end_turn":
                break
            elif ability_choice not in ("move", "move_away") and not self.action_taken:
                self.use_ability(self.arena, ability_choice, opponent)
                self.action_taken = True
            elif ability_choice in ("move", "move_away"):
                self.use_ability(self.arena, ability_choice, opponent)
                self.tiles_moved += 1
            self.arena.present()


    def use_ability(self, arena, name: str, target):

        try:
            self.abilities[name](arena, self, target)
        except Exception as e:
            print(f"fighter.py: {e}")