from enum import Enum, auto
import copy

class RollOptions(Enum):
    RerollOnes = auto()
    RerollFailed = auto()
    NoAutohitSixes = auto()
    NoAutomissOnes = auto()

class Roll:

    def __init__(self, target):
        self.target = target
        self.options = []

    def throw(self):
        target = self.target
        if self.options.count(RollOptions.NoAutohitSixes) == 0:
            target = min(target, 6)
        if self.options.count(RollOptions.NoAutomissOnes) == 0:
            target = max(target, 2)
        base_result = (7-target)/6

        return self.execute_options(base_result)

    def add_option(self, option):
        self.options.append(option)
        return self

    def execute_options(self, base):
        result = base
        for option in self.options:
            if option == RollOptions.RerollOnes:
                result += base/6
            elif option == RollOptions.RerollFailed:
                result += (1-base) * base
        return result

class Weapon:

    def __init__(self, attacks=0, hit=None, wound=None, damage=0, rend=None):

        self.attacks = attacks
        self.hit = hit
        self.wound = wound
        self.damage = damage
        self.rend = rend

    def attack(self, save=None):
        result = self.attacks * self.hit.throw() * self.wound.throw() * self.damage

        if save is not None:
            if self.rend is not None:
                save.target = save.target - self.rend
            result = result * (1- save.throw())

        return result

class Unit:

    def __init__(self):
        self.weapons = []
        self.cost = 0
        self.save = None

    def with_weapons(self, weapon, amount=1):
        unit_weapon = copy.copy(weapon)
        unit_weapon.attacks = weapon.attacks * amount
        self.weapons.append(unit_weapon)
        return self

    def with_cost(self, cost):
        self.cost = cost
        return self

    def with_save(self, save):
        self.save = save.add_option(RollOptions.NoAutohitSixes)
        return self
        
    def attack(self, opponent):
        result = 0
        if opponent.save is not None:
            for weapon in self.weapons:
                result = result + weapon.attack(opponent.save)
            return result
        else:
            for weapon in self.weapons:
                result = result + weapon.attack()
            return result

    def efficiency_against(self, opponent):
        result = self.attack(opponent)
        return (result / self.cost) * 100

def test(first, second):
    diff = first - second
    assert abs(diff) < 0.00001, "Error, " + str(first) + " is not " + str(second)

test(Weapon(attacks=1, hit=Roll(4), wound=Roll(4), damage=1).attack(save=Roll(4)),
        0.125)

test(Weapon(attacks=1, hit=Roll(4).add_option(RollOptions.RerollOnes), wound=Roll(4), damage=1)
        .attack(save=Roll(4)), 0.14583333)

test(Weapon(attacks=2, hit=Roll(3), wound=Roll(5).add_option(RollOptions.RerollFailed), damage=3)
        .attack(save=Roll(6)), 1.85185185185)

