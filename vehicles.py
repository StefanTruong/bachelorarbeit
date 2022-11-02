from tile import Tile
import numpy as np


class Vehicle:
    def __init__(self, speed, tile=None, max_velocity=0):
        self.sim = None
        self.distance_behind_other_lane = None
        self.distance_front_other_lane = None
        self.distance_front = None
        self.speed = speed
        self.maxV = max_velocity
        self.tile = tile
        self.icon = 'Das soll nicht geprinted werden!'

    def calc_dist_front_vehicle(self, lane):
        """
        calculates how much distance is ahead according to left or right lane
        :param lane:
        :return: Integer distance
        """
        my_position = self.tile.get_index()
        my_street = self.sim.tiles
        distance = 0

        while my_street[(my_position + distance + 1) % self.sim.length][lane].vehicle is None:
            distance += 1

            if distance > self.sim.length:
                break

        return distance

    def calc_dist_behind_vehicle(self, lane):
        """
        calculates how much distance it is behind according to left or right lane
        :param lane:
        :return: Integer behind distance
        """
        my_position = self.tile.get_index()
        my_street = self.sim.tiles
        behind_distance = 0

        while my_street[(my_position - behind_distance -1) % self.sim.length][lane].vehicle is None:
            behind_distance += 1

            if behind_distance > self.sim.length:
                break

        return behind_distance

    def look_at_positional_environment(self):
        """
        look at the position of other vehicles
        :return:
        """
        if self.tile.get_lane() == 0:
            other_lane = 1
        elif self.tile.get_lane() == 1:
            other_lane = -1

        # ahead free distance in current lane
        self.distance_front = self.calc_dist_front_vehicle(self.tile.get_lane())

        # ahead free distance in other lane
        self.distance_front_other_lane = self.calc_dist_front_vehicle(self.tile.get_lane() + other_lane)

        # behind free distance in other lane
        self.distance_behind_other_lane = self.calc_dist_behind_vehicle(self.tile.get_lane() + other_lane)

    def look_at_vehicle_at_pos(self, position, lane):
        return self.sim.tiles[position][lane].get_vehicle()

    def switch_possible(self):
        switch = False

        if self.tile.get_lane() == 0:
            other_lane = 1
        elif self.tile.get_lane() == 1:
            other_lane = -1

        # switching only possible if side is free
        if self.sim.tiles[self.tile.get_index()][self.tile.get_lane() + other_lane].get_vehicle() is None:

            # T2 more space than current velocity + 1
            if self.distance_front_other_lane > (self.get_speed() + 1):

                # Look what kind of vehicle is behind me
                look_street_idx = (self.tile.get_index() - self.distance_behind_other_lane) % self.sim.length
                behind_vehicle = self.look_at_vehicle_at_pos(look_street_idx, self.tile.get_lane() + other_lane)

                if behind_vehicle is not None:
                    behind_max_speed = behind_vehicle.get_maxV()
                else:
                    behind_max_speed = 0

                # T3 more space than behind max_speed of rear car
                if self.distance_behind_other_lane > behind_max_speed:

                    # T4 random switch chance
                    if np.random.random() < self.sim.prob_changelane:
                        switch = True

        return switch

    def check_switch_position(self):
        """
        returns a Boolean if vehicle should switch lane
        :return: Boolean to switch_lane
        """
        switch_lane = False

        self.look_at_positional_environment()

        # asymmetric condition for switching lanes L->R see Rickert (T2-T4)
        if self.tile.get_lane() == 0:
            # cars always try to return to the right lane, independent of the situation on the left lane
            switch_lane = self.switch_possible()

        # asymmetric condition for switching lanes R->L see Rickert (T1-T4)
        elif self.tile.get_lane() == 1:
            # current lane ahead has smaller space than current velocity + 1  security tile distance (T1)
            if self.distance_front < self.get_speed() + 1:
                switch_lane = self.switch_possible()

        return switch_lane

    def update_speed(self):
        """
        updates its speed before actual moving. lookat_positional_environment has to be updated first
        :return:
        """
        self.look_at_positional_environment()

        # 1.) Acceleration: accelerate if max speed not achieved if distance allows it. security distance of 1 tile
        if self.distance_front > self.get_speed() + 1 and self.get_speed() < self.get_maxV():
            self.set_speed(self.get_speed() + 1)

        # 2.) Slowing down with one tile security distance
        if self.distance_front <= self.get_speed() != 0:
            self.set_speed(self.distance_front - 1)

        if self.distance_front == 0:
            self.set_speed(0)

        # 3.) Randomization
        if self.get_speed() > 0 and np.random.random() < self.sim.prob_slowdown:
            self.set_speed(self.get_speed() - 1)

    def set_tile(self, tile):
        self.tile = tile

    def set_speed(self, speed):
        self.speed = speed

    def get_tile(self):
        return self.tile

    def get_speed(self):
        return self.speed

    def get_maxV(self):
        return self.maxV

    def get_icon(self):
        return self.icon

    def set_MyTrafficSimulation(self, sim):
        self.sim = sim

    def set_icon(self, symbol):
        speed_str = str(self.get_speed())
        if len(speed_str) == 1:
            self.icon = ' ' + symbol + speed_str + '  '
        elif len(speed_str) == 2:
            self.icon = ' ' + symbol + speed_str + ' '


class Car(Vehicle):
    def __init__(self, speed, tile, max_velocity=12):
        super().__init__(speed, tile, max_velocity)
        self.symbol = 'C'

    def get_icon(self):
        # set_icon has always to be updated with current speed before returned
        super().set_icon(self.symbol)
        return super().get_icon()


class Bike(Vehicle):
    # max_velocity: 35km/h = 10m/s -> 10m/s / 3,75 = 3tiles
    def __init__(self, speed, tile, max_velocity=2):
        super().__init__(speed, tile, max_velocity)
        self.symbol = 'B'

    def get_icon(self):
        super().set_icon(self.symbol)
        return super().get_icon()


class Motorcycle(Vehicle):
    # max_velocity: 100km/h = 30m/s -> 30m/s / 3,75m = 8tiles
    def __init__(self, speed, tile, group, prefered_speed, max_velocity=8):
        """
        initializes Motorcycle with parameters
        :param speed: integer, current initial speed
        :param tile: tile obj, the tile in the street where it is positioned
        :param group: integer, biker group number
        :param prefered_speed: dictionary of prefered spped e.g. {'cautious' : None}
        :param max_velocity:
        :param fun: ToDo
        """
        super().__init__(speed, tile, max_velocity)
        self.ahead = None
        self.behind = None
        self.group = group
        self.prefered_speed = prefered_speed
        self.fun = 0
        self.symbol = 'M'

    def set_behind_partner(self, partner):
        self.behind = partner

    def set_ahead_partner(self, partner):
        self.ahead = partner


    def get_behind_partner(self):
        return self.behind

    def get_ahead_partner(self):
        return self.ahead

    def get_icon(self):
        super().set_icon(self.symbol)
        return super().get_icon()


