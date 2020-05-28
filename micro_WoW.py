from abc import ABC, abstractmethod
from random import randint
import random
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


class Unit:

    _name = None
    _health = 100
    _dmg = 1
    _defence = 10
    _crit_chance = 1.5 if randint(1, 100) >= 50 else 1
    _dodge_chance = 0 if randint(1, 100) >= 80 else 1

    def __init__(self, name, dmg, defence, health, stuff=None):
        super().__init__()
        self._name = name
        self._dmg = dmg
        self._defence = defence
        self._health = health
        if self._health <= 0:
            raise HealthError

        if stuff.needed_class is not None:
            try:
                if self.__class__ not in stuff.needed_class:
                    raise TypeError
            except:
                if stuff.needed_class != self.__class__:
                    raise TypeError

        if stuff.defence_bonus != 0:
            self._defence += stuff.defence_bonus

        if stuff.dmg_bonus != 0:
            self._dmg += stuff.dmg_bonus

        if stuff.health_bonus != 0:
            self._health += stuff.health_bonus

    @abstractmethod
    def attack(self, enemy):
        pass

    @abstractmethod
    def get_dmg(self):
        pass

    @abstractmethod
    def get_defence(self):
        pass

    @abstractmethod
    def _get_health(self, enemy):
        pass

    def _get_health(self, enemy):
        self._health -= enemy._attack
        if self._health <= 0:
            print(f'{self._name} is dead')

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


class Mage(Unit):

    def get_dmg(self):
        return self._dmg

    def get_defence(self):
        return self._defence

    def attack(self, enemy):
        if not isinstance(enemy, Unit):
            raise EnemyError

        if self._health <= 0:
            raise HealthError

        _dmg = self.get_dmg() * self._crit_chance * enemy._dodge_chance
        _defence = enemy.get_defence()
        enemy._health = enemy._health - _dmg + enemy._defence

        if enemy._health <= 0:
            return f'{enemy._name} is dead'
        elif enemy._dodge_chance == 0:
            return f'{enemy._name} dodged the attack'
        else:
            return f'{self._name} attacked {enemy._name}. The health of {enemy._name} is {enemy._health}'

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


class Knight(Unit):

    def get_dmg(self):
        return self._dmg

    def get_defence(self):
        return self._defence

    def attack(self, enemy):
        if not isinstance(enemy, Unit):
            raise EnemyError

        if self._health <= 0:
            raise HealthError

        _dmg = self.get_dmg() * self._crit_chance * enemy._dodge_chance
        _defence = enemy.get_defence()
        enemy._health -= _dmg - (1/2 * _defence)  # скобки для читабельности

        if enemy._health <= 0:
            return f'{enemy._name} is dead'

        elif enemy._dodge_chance == 0:
            return f'{enemy._name} dodged the attack'
        else:
            return f'{self._name} attacked {enemy._name}. The health of {enemy._name} is {enemy._health}'

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


class Stuff:

    needed_class = None
    stuff_name = None
    defence_bonus = None
    dmg_bonus = None
    health_bonus = None

    def __init__(self,  stuff_name, needed_class=None, defence_bonus=0, dmg_bonus=0, health_bonus=0):
        self.stuff_name = stuff_name
        self.defence_bonus = defence_bonus
        self.dmg_bonus = dmg_bonus
        self.health_bonus = health_bonus
        self.needed_class = needed_class


nothing = Stuff('nothing')  # write in character stuff if he doesn't have anything

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


class Battle:

    modifications = {
        Mage: {
            '_health': 10,
            '_defence': 50,
            '_dmg': 20},
        Knight: {
            '_health': 20,
            '_defence': 10,
            '_dmg': 30}
    }

    def __init__(self, unit1, unit2):
        if not isinstance(unit1, Unit) or not isinstance(unit2, Unit):
            raise Exception

        self.unit1 = unit1
        self.unit2 = unit2

    def deploy_mods_into_unit(self, unit):
        key = unit.__class__
        mods = self.modifications[key]

        for i in mods:
            attr = getattr(unit, i, None)

            if isinstance(attr, (int, float)):

                val = attr + mods[i]
                setattr(unit, i, val)

        return unit

    def decide_first(self):

        arr = [self.unit1, self.unit2]
        random.shuffle(arr)
        return arr

    def start_battle(self):
        self.unit1 = self.deploy_mods_into_unit(self.unit1)
        self.unit2 = self.deploy_mods_into_unit(self.unit2)
        lst = self.decide_first()
        self.unit1 = lst[0]
        self.unit2 = lst[1]

        while True:
            print(self.unit1.attack(self.unit2))
            if self.unit2._health <= 0:
                return self.unit1

            print(self.unit2.attack(self.unit1))
            if self.unit1._health <= 0:
                return self.unit2


python = Mage("Python", 100, 100, 300, nothing)
pascal = Knight("Pascal", 75, 75, 250, nothing)

lng_battle = Battle(python, pascal)
lng_battle.start_battle()
