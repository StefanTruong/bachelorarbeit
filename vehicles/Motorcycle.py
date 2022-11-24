from vehicles.Vehicles import *


# --------------------------------------------------------------------------------------------------------------------
class Motorcycle(Vehicle):
    # max_velocity: 100km/h = 30m/s -> 30m/s / 3,75m = 8tiles
    def __init__(self, speed, tile, group, preferred_speed, max_velocity=7):
        """
        initializes Motorcycle with parameters
        :param speed: integer, current initial speed
        :param tile: tile obj, the tile in the street where it is positioned
        :param group: integer, biker group number
        :param preferred_speed: dictionary of preferred speed e.g. {'cautious' : None}
        :param max_velocity:
        :param fun: ToDo
        """
        super().__init__(speed, tile, max_velocity)
        # security distance of 2 sec. 60km/h ~ 16m/s ~ 4tiles ~ 8tiles
        self.security_distance = 8
        self.distance_behind_partner = 0
        self.distance_ahead_partner = 0
        self.ahead = None
        self.behind = None
        self.group = group
        self.preferred_speed = preferred_speed
        self.fun = 0
        self.symbol = 'M'

    def update_speed(self):
        """
        updates its speed before actual moving. lookat_positional_environment has to be updated first
        :return:
        """
        self.look_at_positional_environment()
        self.calc_distance_behind_partner()
        self.calc_distance_ahead_partner()

        # 1. Acceleration: accelerate if max speed not achieved if distance allows it. No security distance of 1 tile
        # cannot accelerate more than tile speed limit
        if self.distance_front > self.get_speed() and self.get_speed() < self.get_maxV()\
                and self.get_speed() < self.get_tile().get_speed_limit():

            # additional acceleration if too far from ahead partner
            if self.distance_front > self.get_speed() + self.catch_up() and \
                    self.get_speed() + self.catch_up() < self.get_maxV() and \
                    self.get_speed() + self.catch_up() < self.get_tile().get_speed_limit():
                self.set_speed(self.get_speed() + self.catch_up() + 1)

            else:
                self.set_speed(self.get_speed() + 1)

        # 2. slowdown if too far from behind partner
        # in case of first and second if statement are true, then offset initial catch_up speed
        if self.distance_behind_partner > self.get_speed() + self.slow_down() > 0:
            # consider what speed the vehicle behind has before slowing down
            this_is_my_lane = self.get_tile().get_lane()
            this_is_distance_behind = self.distance_behind
            behind_vehicle = self.look_at_vehicle_at_pos(self.distance_behind, self.get_tile().get_lane())

            if behind_vehicle is not self.get_behind_partner():
                if self.distance_behind > self.get_speed() + self.slow_down() > 0:
                    self.set_speed(self.get_speed() + self.slow_down())

        # 3. Slowing down with no tile security distance. No security distance
        if self.distance_front <= self.get_speed() != 0:
            self.set_speed(self.distance_front)

        # 4. Cannot be faster than allowed speed limit of the current tile
        if self.get_speed() > self.get_tile().get_speed_limit():
            self.set_speed(self.get_tile().get_speed_limit())

        # 5. Stop if there is no space in front
        if self.distance_front == 0:
            self.set_speed(0)

        # 6. Randomization
        if self.get_speed() > 0 and np.random.random() < self.sim.prob_slowdown:
            self.set_speed(self.get_speed() - 1)

        self.update_partners()

    def catch_up(self):
        """
        speed up velocity if ahead partner motorcyclist is too far away. Ignores other vehicles
        :param current_speed: the current speed of the vehicle
        :return:
        """
        speed_up = 0
        if self.get_ahead_partner() is not None:
            if self.distance_ahead_partner > self.security_distance > self.get_speed():
                speed_up = 1

        return speed_up

    def slow_down(self):
        """
        slow down speed if behind partner motorcyclist is too far away. Ignores other vehicles
        :param current_speed:
        :return:
        """
        slow_down = 0
        if self.get_behind_partner() is not None:
            if self.distance_behind_partner > self.security_distance > self.get_speed():
                slow_down = -1

        return slow_down

    def calc_distance_behind_partner(self):
        """
        calculates how far the distance the motorcyclist behind is
        :return:
        """
        if self.get_behind_partner() is not None:
            self.distance_behind_partner = (self.get_tile().get_index() -
                                            self.get_behind_partner().get_tile().get_index()) % self.sim.length

    def calc_distance_ahead_partner(self):
        """
        calculates how far the distance the motorcyclist ahead is
        :return:
        """
        if self.get_ahead_partner() is not None:
            self.distance_ahead_partner = (self.get_ahead_partner().get_tile().get_index() -
                                           self.get_tile().get_index()) % self.sim.length

    def update_partners(self):
        """
        updates the partners of the motorcyclist
        :return:
        """
        idx_front_in_position = False
        idx_behind_in_position = False

        while not (idx_front_in_position and idx_behind_in_position):
            # current motorcyclist overtakes ahead partner
            if self.get_ahead_partner() is not None:
                if self.get_ahead_partner().get_tile().get_index() < self.get_tile().get_index():
                    old_ahead_partner = self.get_ahead_partner()
                    old_behind_partner = self.get_behind_partner()
                    self.set_ahead_partner(self.get_ahead_partner().get_ahead_partner())
                    self.set_behind_partner(old_ahead_partner)
                    old_ahead_partner.set_ahead_partner(self)
                    old_ahead_partner.set_behind_partner(old_behind_partner)
                else:
                    idx_front_in_position = True
            else:
                idx_front_in_position = True

            # behind partner overtakes current motorcyclist
            if self.get_behind_partner() is not None:
                if self.get_behind_partner().get_tile().get_index() > self.get_tile().get_index():
                    old_ahead_partner = self.get_ahead_partner()
                    old_behind_partner = self.get_behind_partner()
                    self.set_behind_partner(self.get_behind_partner().get_behind_partner())
                    self.set_ahead_partner(old_behind_partner)
                    old_behind_partner.set_behind_partner(self)
                    old_behind_partner.set_ahead_partner(old_ahead_partner)
                else:
                    idx_behind_in_position = True
            else:
                idx_behind_in_position = True

    def check_switch_position(self):
        """
        returns a Boolean if Motorcyclist should switch lane. Will not switch lane if platoon member is directly ahead
        :return: Boolean to switch_lane
        """
        switch_lane = False

        self.look_at_positional_environment()

        # asymmetric condition for switching lanes L->R see Rickert (T2-T4)
        if self.tile.get_lane() == 0:

            # cars always try to return to the right lane, independent of the situation on the left lane
            switch_lane = self.switch_possible()

            # do not switch if direct vehicle ahead is a platoon member
            # Hint self.distance_front + 1 mandatory, since distance_front calculates the actual empty distance
            vehicle = self.look_at_vehicle_at_pos(self.distance_front + 1, self.tile.get_lane())
            if type(vehicle) is Motorcycle and vehicle.get_group() == self.get_group():
                switch_lane = False

        # asymmetric condition for switching lanes R->L see Rickert (T1-T4)
        elif self.tile.get_lane() == 1:

            # current lane ahead has smaller space than current velocity + 1  security tile distance (T1)
            if self.distance_front < self.get_speed() + 1:
                switch_lane = self.switch_possible()

            # do not switch lane if direct vehicle ahead is a platoon member
            # Hint self.distance_front + 1 mandatory, since distance_front calculates the actual empty distance
            vehicle = self.look_at_vehicle_at_pos(self.distance_front + 1, self.tile.get_lane())
            if type(vehicle) is Motorcycle and vehicle.get_group() == self.get_group():
                switch_lane = False

        return switch_lane

    def set_behind_partner(self, partner):
        self.behind = partner

    def set_ahead_partner(self, partner):
        self.ahead = partner

    def get_behind_partner(self):
        return self.behind

    def get_ahead_partner(self):
        return self.ahead

    def get_group(self):
        return self.group

    def get_distance_behind_partner(self):
        return self.distance_behind_partner

    def get_distance_ahead_partner(self):
        return self.distance_ahead_partner

    def get_icon(self):
        super().set_icon(self.symbol)
        return super().get_icon()
