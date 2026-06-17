import fighter
import dice

def execute(attacker: fighter.Fighter, defender: fighter.Fighter):
    attacker_roll = dice.general_roll(attacker, "brawl")
    
    
    if eval(defender.dodge_if):

        attacker_success = dice.general_roll(attacker, "brawl")
        defender_success = dice.general_roll(defender, "dodge")

        if attacker_success > defender_success:
            damage = dice.roll(1, 3)
            defender.take_damage(damage)
            print(f"{attacker.name} punches {defender.name}!")
        elif defender_success <= attacker_success:
            print(f"{defender.name} dodges a punch from {attacker.name}!")
    else:
        attacker_success = dice.general_roll(attacker, "brawl")
        defender_success = dice.general_roll(defender, "brawl")

        if attacker_success > defender_success:
            damage = dice.roll(1, 3)
            defender.take_damage(damage)
            print(f"{attacker.name} punches {defender.name}!")
        elif defender_success > attacker_success:
            damage = dice.roll(1, 3)
            print(f"{defender.name} blocks a punch from {attacker.name}!")
            print(f"{defender.name} deals {damage} damage in the process!")
            attacker.take_damage(dice.roll(1, 3), False)
        else:
            print(f"{attacker.name} fails to effectively punch {defender.name}, dealing no damage!")