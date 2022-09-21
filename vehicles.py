from tile import Tile


class Vehicle:
    def __init__(self, speed, tile=None, max_velocity=0):
        self.speed = speed
        self.maxV = max_velocity
        self.tile = tile


class Car(Vehicle):
    def __init__(self, speed, tile, max_velocity=10):
        super().__init__(speed, tile, max_velocity)


class Bike(Vehicle):
    def __init__(self, speed, tile, max_velocity=3):
        super().__init__(speed, tile, max_velocity)


class Motorcycle(Vehicle):
    def __init__(self, speed, tile, group, prefered_speed, max_velocity=6):
        super().__init__(speed, tile, max_velocity)
        self.group = group
        self.prefered_speed = prefered_speed
        self.fun = 0

