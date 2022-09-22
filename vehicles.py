from tile import Tile


class Vehicle:
    def __init__(self, speed, tile=None, max_velocity=0):
        self.speed = speed
        self.maxV = max_velocity
        self.tile = tile
        self.icon = 'Das soll nicht geprinted werden!'

    def set_tile(self, tile):
        self.tile = tile

    def get_tile(self):
        return self.tile

class Car(Vehicle):
    def __init__(self, speed, tile, max_velocity=10):
        super().__init__(speed, tile, max_velocity)
        self.icon = 'C'


class Bike(Vehicle):
    def __init__(self, speed, tile, max_velocity=3):
        super().__init__(speed, tile, max_velocity)
        self.icon = 'B'


class Motorcycle(Vehicle):
    def __init__(self, speed, tile, group, prefered_speed, max_velocity=6):
        super().__init__(speed, tile, max_velocity)
        self.ahead = None
        self.behind = None
        self.icon = 'M'
        self.group = group
        self.prefered_speed = prefered_speed
        self.fun = 0

    def set_behind_partner(self, partner):
        self.behind = partner

    def set_ahead_partner(self, partner):
        self.ahead = partner

    def get_behind_partner(self):
        return self.behind

    def get_ahead_partner(self):
        return self.ahead

