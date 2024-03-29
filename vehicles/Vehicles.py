import numpy as np


class Vehicle:
    def __init__(self, speed, tile=None, max_velocity=0):
        self.sim = None
        self.distance_behind_other_lane = None
        self.distance_front_other_lane = None
        self.distance_front = None
        self.distance_behind = None
        self.speed = speed
        self.maxV = max_velocity
        self.tile = tile
        self.icon = 'Das soll nicht geprinted werden!'
        self.id = 666

        # values if the motorcyclist has moved in the current time step. see moving_each_vehicle in MyTrafficSimulation
        # Will be first moved forward then switch position vehicle by vehicle
        self.moved = False

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

        while my_street[(my_position - behind_distance - 1) % self.sim.length][lane].vehicle is None:
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

        # behind free distance in current lane
        self.distance_behind = self.calc_dist_behind_vehicle(self.tile.get_lane())

        # ahead free distance in other lane
        self.distance_front_other_lane = self.calc_dist_front_vehicle(self.tile.get_lane() + other_lane)

        # behind free distance in other lane
        self.distance_behind_other_lane = self.calc_dist_behind_vehicle(self.tile.get_lane() + other_lane)

    def look_at_vehicle_at_pos(self, position, lane):
        pos = position % self.sim.length
        return self.sim.tiles[pos][lane].get_vehicle()

    def switch_possible(self):
        switch = False

        if self.tile.get_lane() == 0:
            other_lane = 1
        elif self.tile.get_lane() == 1:
            other_lane = -1

        # switching only possible if side is free
        if self.sim.tiles[self.tile.get_index()][self.tile.get_lane() + other_lane].get_vehicle() is None:

            # Look what kind of vehicle is behind me. Todo check if -1 for look_street_idx is correct
            if self.distance_front_other_lane > (self.get_speed() + 1):
                # removed rule. Don't know why it is here
                    #and \
                    #self.get_speed() < self.get_tile().get_speed_limit():

                # Look what kind of vehicle is behind me. Todo check if -1 for look_street_idx is correct
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

        # 1. Acceleration: accelerate if max speed not achieved if distance allows it. security distance of 1 tile
        # Cannot be faster than allowed speed limit of the current tile
        if self.distance_front > self.get_speed() + 1 and self.get_speed() < self.get_maxV()\
                and self.get_speed() < self.get_tile().get_speed_limit():
            self.set_speed(self.get_speed() + 1)

        # 2. Slowing down with one tile security distance
        if self.distance_front <= self.get_speed() != 0:
            self.set_speed(self.distance_front - 1)

        # 3. Cannot be faster than allowed speed limit of the current tile
        if self.get_speed() > self.get_tile().get_speed_limit():
            self.set_speed(self.get_tile().get_speed_limit())

        # 4. Stop if distance is 0
        if self.distance_front == 0:
            self.set_speed(0)

        # 5. Randomization
        if self.get_speed() > 0 and np.random.random() < self.sim.prob_slowdown:
            self.set_speed(self.get_speed() - 1)

    def set_tile(self, tile):
        self.tile = tile

    def set_speed(self, speed):
        self.speed = speed

    def set_id(self, identifier):
        self.id = identifier

    def get_tile(self):
        return self.tile

    def get_speed(self):
        return self.speed

    def get_maxV(self):
        return self.maxV

    def get_icon(self):
        return self.icon

    def get_id(self):
        return self.id

    def get_moved(self):
        return self.moved

    def get_type(self):
        return type(self).__name__

    def get_icon_granular(self):
        return '.'

    def get_role(self):
        return None

    def set_MyTrafficSimulation(self, sim):
        self.sim = sim

    def set_icon(self, symbol):
        speed_str = str(self.get_speed())
        if len(speed_str) == 1:
            self.icon = '' + symbol + speed_str + '   '
        elif len(speed_str) == 2:
            self.icon = '' + symbol + speed_str + '  '
        elif len(speed_str) == 3:
            self.icon = '' + symbol + speed_str + ' '

    def set_moved(self, moved=False):
        self.moved = moved


# --------------------------------------------------------------------------------------------------------------------
class Car(Vehicle):
    def __init__(self, speed, tile, max_velocity=10):
        """
        :param speed:
        :param tile:
        :param max_velocity: max Velocity of a vehicle in the model has the Car. If changed then update_flow_all_lanes
        at Analyzer.py has to be changed as well!
        """
        super().__init__(speed, tile, max_velocity)
        self.symbol = 'C'

    def get_icon(self):
        # set_icon has always to be updated with current speed before returned
        super().set_icon(self.symbol)
        return super().get_icon()

    def set_symbol(self, symbol):
        self.symbol = symbol


# --------------------------------------------------------------------------------------------------------------------
class Bike(Vehicle):
    # max_velocity: 35km/h = 10m/s -> 10m/s / 3,75 = 3tiles
    def __init__(self, speed, tile, max_velocity=2):
        super().__init__(speed, tile, max_velocity)
        self.symbol = 'B'

    def switch_possible(self):
        """
        Checks if a switch to the right lane is possible. A Bike will switch if
        will only be called when the Bike is on the left lane but wants to switch to the right lane
        :return:
        """
        switch = False

        if self.tile.get_lane() == 0:
            other_lane = 1
        elif self.tile.get_lane() == 1:
            other_lane = -1

        # switching only possible if side is free
        if self.sim.tiles[self.tile.get_index()][self.tile.get_lane() + other_lane].get_vehicle() is None:
            switch = True

        return switch

    def check_switch_position(self):
        """
        returns a Boolean if Bike should switch lane. A Bike only switches to the right lane and will stay there
        :return: Boolean to switch_lane
        """
        switch_lane = False

        self.look_at_positional_environment()

        # asymmetric condition for switching lanes L->R see Rickert (T2-T4)
        if self.tile.get_lane() == 0:
            # cars always try to return to the right lane, independent of the situation on the left lane
            switch_lane = self.switch_possible()

        # a Bile should never switch to the left lane since it knows that it is too slow
        elif self.tile.get_lane() == 1:
            pass

        return switch_lane

    def update_speed(self):
        """
        updates its speed before actual moving. lookat_positional_environment has to be updated first
        :return:
        """
        self.look_at_positional_environment()

        # 1. Acceleration: accelerate if max speed not achieved if distance allows it. No security distance
        # Cannot be faster than allowed speed limit of the current tile
        if self.distance_front > self.get_speed() and self.get_speed() < self.get_maxV()\
                and self.get_speed() < self.get_tile().get_speed_limit():
            self.set_speed(self.get_speed() + 1)

        # 2. Slowing down with no tile security distance. No security distance
        if self.distance_front <= self.get_speed() != 0:
            self.set_speed(self.distance_front)

        # 3. Cannot be faster than allowed speed limit of the current tile
        if self.get_speed() > self.get_tile().get_speed_limit():
            self.set_speed(self.get_tile().get_speed_limit())

        # 4. Stop if there is no space in front
        if self.distance_front == 0:
            self.set_speed(0)

        # 5. Randomization
        if self.get_speed() > 0 and np.random.random() < self.sim.prob_slowdown:
            self.set_speed(self.get_speed() - 1)

    def get_icon(self):
        super().set_icon(self.symbol)
        return super().get_icon()

    def set_symbol(self, symbol):
        self.symbol = symbol
