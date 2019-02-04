from enum import Enum, auto

class RollOptions(Enum):
    RerollOnes = auto()
    RerollFailed = auto()

def calculate_option(option, base):
    if option == RollOptions.RerollOnes:
        return base/6
    elif option == RollOptions.RerollFailed:
        return (1-base) * base
    return 0

class Roll:

    def __init__(self, target):
        self.target = target
        self.options = []

    def throw(self):
        target = min(max(self.target,2), 6)
        base_result = (7-target)/6

        return self.execute_options(base_result)

    def add_option(self, option):
        self.options.append(option)

    def execute_options(self, base):
        result = base
        for option in self.options:
            result = result + calculate_option(option, base)
        return result

class Weapon:

    def __init__(self, attacks=0, hit=6, wound=6, damage=0,
        reroll_ones_hit=None, reroll_ones_wound=None,
        reroll_failed_hits=None, reroll_failed_wounds=None):

        self.attacks = attacks
        self.hit = Roll(hit)
        self.wound = Roll(wound)
        self.damage = damage

        if reroll_ones_hit == True: self.hit.add_option(RollOptions.RerollOnes)
        if reroll_failed_hits == True: self.hit.add_option(RollOptions.RerollFailed)

        if reroll_ones_wound == True: self.wound.add_option(RollOptions.RerollOnes)
        if reroll_failed_wounds == True: self.wound.add_option(RollOptions.RerollFailed)

    def attack(self, save=None, reroll_ones_save=None, reroll_failed_saves=None):
        result = self.attacks * self.hit.throw() * self.wound.throw() * self.damage

        if type(save) == int:
            save_roll = Roll(save)

            if reroll_ones_save == True: save_roll.add_option(RollOptions.RerollOnes)
            if reroll_failed_saves == True: save_roll.add_option(RollOptions.RerollFailed)

            result = result * (1- save_roll.throw())

        return result


def weapon_roller(attacks=0, hit=6, wound=6, damage=0, save=None,
        reroll_ones_hit=None, reroll_ones_wound=None, reroll_failed_hits=None, reroll_failed_wounds=None):
    hit_roll = Roll(hit)
    if reroll_ones_hit == True: hit_roll.add_option(RollOptions.RerollOnes)
    if reroll_failed_hits == True: hit_roll.add_option(RollOptions.RerollFailed)

    wound_roll = Roll(wound)
    if reroll_ones_wound == True: wound_roll.add_option(RollOptions.RerollOnes)
    if reroll_failed_wounds == True: wound_roll.add_option(RollOptions.RerollFailed)

    result = attacks * hit_roll.throw() * wound_roll.throw() * damage
    if save is not None:
        save_roll = Roll(save)
        result = result * (1- save_roll.throw())
    return result


def test(first, second):
    diff = first - second
    assert abs(diff) < 0.00001, "Error, " + str(first) + " is not " + str(second)

test(Weapon(attacks=1, hit=4, wound=4, damage=1).attack(save=4), 0.125)
test(Weapon(attacks=1, hit=4, reroll_ones_hit=True, wound=4, damage=1).attack(save=4), 0.14583333)
test(Weapon(attacks=2, hit=3, wound=5, reroll_failed_wounds=True, damage=3).attack(save=6), 1.85185185185)
