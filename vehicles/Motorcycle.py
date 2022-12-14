from vehicles.Vehicles import *


# --------------------------------------------------------------------------------------------------------------------
class Motorcycle(Vehicle):
    # max_velocity: 100km/h = 30m/s -> 30m/s / 3,75m = 8tiles
    def __init__(self, speed, tile, group, preferred_speed, speed_distance_preferences=None, max_velocity=7):
        """
        initializes Motorcycle with parameters
        :param speed: integer, current initial speed
        :param tile: tile obj, the tile in the street where it is positioned
        :param group: integer, biker group number
        :param preferred_speed: dictionary of preferred speed. Available: 'speed', 'average', 'cautious'
        see config speed_preferences
        :param speed_distance_preferences: dict how far the distance should be for speed type
        see config speed_distance_preferences
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
        self.symbol = 'M'

        # motorcyclist speed and distance preferences and weightings
        self.speed_preference = preferred_speed
        self.current_speed_preference = None
        self.behind_gap_preference = None
        self.front_gap_preference = None
        self.inbetween_gap_preference = None
        self.behind_gap_ampl = None
        self.front_gap_ampl = None
        self.speed_ampl = None
        self.fun_weight = None

        # Position of motorcyclist
        self.is_leader = False
        self.is_sweeper = False
        self.is_inbetween = False

        # list of all platoon members
        self.my_platoon = []

        self.fun = 0

    def update_speed(self):
        """
        updates its speed before actual moving. lookat_positional_environment has to be updated first
        :return:
        """
        self.look_at_positional_environment()
        self.update_partners()

        # 1. Acceleration: accelerate if max speed not achieved if distance allows it. No security distance of 1 tile
        # cannot accelerate more than tile speed limit
        if self.distance_front > self.get_speed() and self.get_speed() < self.get_maxV() \
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
            behind_vehicle = self.look_at_vehicle_at_pos(self.get_tile().get_index() - self.distance_behind,
                                                         self.get_tile().get_lane())

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

    # todo check if this is finale version
    def update_speed_with_preference(self):
        """
        first the leader adjust its distance. All other motorcyclist adjust to the ahead partner distance
        :return:
        """
        self.look_at_positional_environment()
        self.update_partners()
        self.update_preferences(self.tile.get_curvature())

        close_up_dist_behind = self.estimate_close_up_distance('behind')
        close_up_dist_ahead = self.estimate_close_up_distance('ahead')

        # the leader decides the speed of the platoon
        if self.is_leader:
            if self.tile.get_lane() == 0:
                other_lane = 1
            elif self.tile.get_lane() == 1:
                other_lane = -1
            look_street_idx = (self.tile.get_index() - self.distance_behind_other_lane - 1) % self.sim.length
            behind_vehicle_other_lane = self.look_at_vehicle_at_pos(look_street_idx, self.tile.get_lane() + other_lane)
            behind_vehicle = self.look_at_vehicle_at_pos(
                self.get_tile().get_index() - self.distance_behind - 1, self.tile.get_lane())

            # on the left lane
            if self.get_tile().get_lane() == 1:
                # accelerate if behind distance is too near
                if close_up_dist_behind < self.behind_gap_preference:

                    # Acceleration: accelerate if max speed not achieved if distance allows it. No security 1 tile
                    # cannot accelerate more than tile speed limit
                    if self.distance_front > self.get_speed() and self.get_speed() < self.get_maxV() \
                            and self.get_speed() < self.get_tile().get_speed_limit():
                        self.set_speed(self.get_speed() + 1)

                # Decelerate if behind distance is too far. Cannot be under zero
                if close_up_dist_behind > self.behind_gap_preference and self.get_speed() > 0:
                    self.set_speed(self.get_speed() - 1)

                # Hold optimal distance. Accelerate or Decelerate if not speed_preference achieved
                if close_up_dist_behind == self.behind_gap_preference:
                    if self.get_speed() < self.current_speed_preference:
                        if self.distance_front > self.get_speed() and self.get_speed() < self.get_maxV() \
                                and self.get_speed() < self.get_tile().get_speed_limit():
                            self.set_speed(self.get_speed() + 1)

                    elif self.get_speed() > self.current_speed_preference and self.get_speed() > 0:
                        self.set_speed(self.get_speed() - 1)

            # on the right lane. Leader want to overtake something. Get max speed even violating speed preference
            else:
                # Acceleration: accelerate if max speed not achieved if distance allows it. No security 1 tile
                # cannot accelerate more than tile speed limit
                if self.distance_front > self.get_speed() and self.get_speed() < self.get_maxV() \
                        and self.get_speed() < self.get_tile().get_speed_limit():
                    self.set_speed(self.get_speed() + 1)

            # todo implement recursive distance berechnung
            # calc_platoon_distance = self.platoon_distance_too_far()
        else:
            # the sweeper and inbetween motorcyclists follow the ahead_partner if he is insight
            ahead_vehicle = self.look_at_vehicle_at_pos(self.get_tile().get_index() + self.distance_front + 1,
                                                        self.tile.get_lane())
            partner_in_sight = False
            if ahead_vehicle is self.get_ahead_partner():
                partner_in_sight = True

            if partner_in_sight:
                # accelerate if ahead distance too far
                if close_up_dist_ahead > self.front_gap_preference:
                    # Acceleration: accelerate if max speed not achieved if distance allows it. No security of 1 tile
                    # cannot accelerate more than tile speed limit
                    if self.distance_front > self.get_speed() and self.get_speed() < self.get_maxV() \
                            and self.get_speed() < self.get_tile().get_speed_limit():
                        self.set_speed(self.get_speed() + 1)
                    # Decelerate if ahead distance too near
                if close_up_dist_ahead < self.front_gap_preference and self.get_speed() > 0:
                    self.set_speed(self.get_speed() - 1)
                # Hold optimal distance. No acceleration or deceleration for sweeper and inbetween motorcyclists
                if close_up_dist_ahead == self.front_gap_preference:
                    pass
            else:
                # if not partner in sight, adjust speed to speed_preference
                if self.get_speed() < self.current_speed_preference:
                    if self.distance_front > self.get_speed() and self.get_speed() < self.get_maxV() \
                            and self.get_speed() < self.get_tile().get_speed_limit():
                        self.set_speed(self.get_speed() + 1)
                elif self.get_speed() > self.current_speed_preference and self.get_speed() > 0:
                    self.set_speed(self.get_speed() - 1)
                else:
                    pass

        # general_speed_adjustments for all scenarios
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

        # #
        # ToDo update fun

    # todo implement if preference only possible
    def deleted_update_speed_preferenceV4(self):
        """
        updates its speed with regard to its preference before actual moving
        lookat_positional_environment has to be updated first
        :return:
        """
        self.look_at_positional_environment()
        self.update_partners()

        peak = self.estimate_close_up_distance(self.tile.get_curvature())
        # zeiger = self.fun_weight * self.speed
        zeiger = self.speed

        # Todo leader logic for take over
        ahead_vehicle = self.look_at_vehicle_at_pos(self.get_tile().get_index() + self.distance_front + 1,
                                                    self.tile.get_lane())
        behind_vehicle = self.look_at_vehicle_at_pos(self.get_tile().get_index() - self.distance_behind - 1,
                                                     self.tile.get_lane())

        # Check if the motorcyclist is within platoon
        partner_in_sight = False
        ahead_vehicle_same_group = False
        behind_vehicle_same_group = False
        if type(ahead_vehicle) is Motorcycle or type(behind_vehicle) is Motorcycle:
            partner_in_sight = True
            if ahead_vehicle is not None:
                if ahead_vehicle.get_group() == self.get_group():
                    ahead_vehicle_same_group = True
            elif behind_vehicle is not None:
                if behind_vehicle.get_group() == self.get_group():
                    behind_vehicle_same_group = True

        # At least one partner has to be in sight
        if partner_in_sight and (
                ahead_vehicle_same_group or behind_vehicle_same_group) or self.is_leader or self.is_sweeper:
            # accelerate
            if zeiger < peak:
                if self.distance_front > self.get_speed() and self.get_speed() < self.get_maxV() \
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

            # hold current velocity
            # todo evtl. build in tolerance
            elif zeiger == peak:
                # 1. only slow down if there is not much space in front
                if self.distance_front <= self.get_speed() != 0:
                    self.set_speed(self.distance_front)
                # 2. Cannot be faster than allowed speed limit of the current tile
                if self.get_speed() > self.get_tile().get_speed_limit():
                    self.set_speed(self.get_tile().get_speed_limit())
                # 4. Stop if there is no space in front
                if self.distance_front == 0:
                    self.set_speed(0)
                # 5. Randomization
                if self.get_speed() > 0 and np.random.random() < self.sim.prob_slowdown:
                    self.set_speed(self.get_speed() - 1)
            # slow down
            else:
                # 1. slow down if bigger than zero
                if self.get_speed() > 0:
                    self.set_speed(self.get_speed() - 1)
                # 2. definitely slow down if there is not much space in front
                if self.distance_front <= self.get_speed() != 0:
                    self.set_speed(self.distance_front)
                # 3. Cannot be faster than allowed speed limit of the current tile
                if self.get_speed() > self.get_tile().get_speed_limit():
                    self.set_speed(self.get_tile().get_speed_limit())

        # if the motorcyclist has lost the platoon. Neither behind nor front vehicle is motorcyclist of same group
        else:
            # only if motorcyclist is the leader he has to wait all others behave like normal vehicles
            # one speed less than he would like to have
            '''
            if self.is_leader:
                # will not stand still
                if self.get_speed() == 0:
                    self.set_speed(self.get_speed() + 1)
                # 2. Slowing down with no tile security distance. No security distance
                if self.distance_front <= self.get_speed() != 0:
                    self.set_speed(self.distance_front)
                # 3. Stop if there is no space in front
                if self.distance_front == 0:
                    self.set_speed(0)
                # 5. Randomization
                if self.get_speed() > 0 and np.random.random() < self.sim.prob_slowdown:
                    self.set_speed(self.get_speed() - 1)
            '''

            # Normal Behaviour
            # 1. Acceleration: accelerate if max speed not achieved if distance allows it. No security of 1 tile
            # cannot accelerate more than tile speed limit
            if self.distance_front > self.get_speed() and self.get_speed() < self.get_maxV() \
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

        # ToDo update fun

    # todo delete if not used anymore
    def platoon_distance_too_far(self):
        """
        calculates if the overall distance of the platoon is too far. Only the leader adjust its speed to platoon spread
        :return: boolean if leader should slow down
        """
        if self.is_leader:
            overall_gap_distance = 0
            last_motorcycle_position = 0
            current_motorcycle = self
            while current_motorcycle.get_behind_partner() is not None:
                overall_gap_distance += self.estimate_close_up_distance('behind')
                current_motorcycle = current_motorcycle.get_behind_partner()
            last_motorcycle_position = current_motorcycle.get_tile().get_index()
        else:
            raise Exception("Only leader can check if platoon distance is too far")

    def update_preferences(self, current_curvature):
        """
        updates the preferences and weights for acceleration/deacceleration logic
        :param current_curvature:
        :return:
        """
        self.current_speed_preference = self.sim.get_config_object(). \
            get_speed_preference(self.speed_preference, current_curvature)

        self.behind_gap_preference, self.front_gap_preference, self.inbetween_gap_preference = \
            self.sim.get_config_object().get_distance_preference(self.speed_preference)

        self.behind_gap_ampl, self.front_gap_ampl = self.sim.get_config_object(). \
            get_distance_weight(self.speed_preference)

        self.speed_ampl = self.sim.get_config_object(). \
            get_speed_weight(self.speed_preference)

        self.fun_weight = self.sim.get_config_object().get_curve_fun_weight(current_curvature)

    # ToDo delete if not used anymore
    def tobedeleted_calc_peak_value(self, current_curvature):
        """
        calculates the peak value of the merged pdf
        :param current_curvature:   what curvature has the current tile
        speed_peak:          speed mean preference according to curvature
        ahead_dist_peak:     distance mean preference to the vehicle in front used for the sweeper
        behind_dist_peak:    distance mean preference to the vehicle behind used for the leader
        tolerance:           tolerance of the peak value location of the merged pdf
        :return:                    overall peak value
        """
        # update preferences according to current curvature
        self.update_preferences(current_curvature)

        # if motorcyclist is inbetween
        if self.is_inbetween:
            peak = self.fun_weight * self.speed_ampl * self.current_speed_preference + \
                   (self.behind_gap_ampl * self.behind_gap_preference -
                    self.front_gap_ampl * self.front_gap_preference)
        # if motorcyclist is sweeper
        elif self.is_sweeper:
            peak = self.fun_weight * self.speed_ampl * self.current_speed_preference + \
                   (self.front_gap_ampl * self.front_gap_preference -
                    self.front_gap_ampl * self.get_distance_ahead_partner())
        # else motorcyclist is leader
        elif self.is_leader:
            peak = self.fun_weight * self.speed_ampl * self.current_speed_preference + \
                   (self.behind_gap_ampl * (self.get_distance_behind_partner()) -
                    self.behind_gap_ampl * self.behind_gap_preference)
        else:
            raise ValueError("Motorcyclist location not in a group")

        # should at least be 1
        if peak <= 0:
            paek = 1

        return peak

    # todo check distance to partner
    def estimate_close_up_distance(self, partner):
        """
        calculates the distance ahead and behind if current speed wouldn't be changed
        :param partner: 'behind' or 'ahead'. The partner to which the distance is calculated
        :return: close_up_dist estimation of the distance_behind_partner for the next step
        """
        close_up_dist = 0
        if partner == 'behind' and not self.is_sweeper:
            partner_moved = self.get_behind_partner().get_moved()
            if partner_moved:
                close_up_dist = self.get_distance_behind_partner() + self.get_speed()
            else:
                close_up_dist = \
                    self.get_distance_behind_partner() - self.get_behind_partner().get_speed() + self.get_speed()
        elif partner == 'ahead' and not self.is_leader:
            partner_moved = self.get_ahead_partner().get_moved()
            if partner_moved:
                close_up_dist = self.get_distance_ahead_partner() - self.get_speed()
            else:
                close_up_dist = \
                    self.get_distance_ahead_partner() + self.get_ahead_partner().get_speed() - self.get_speed()
        else:
            # if self is leader he does not have a partner ahead. if self is sweeper he does not have a partner behind
            pass

        return close_up_dist

    def catch_up(self):
        """
        speed up velocity if ahead partner motorcyclist is too far away. Ignores other vehicles
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
        :return:
        """
        slow_down = 0
        if self.get_behind_partner() is not None:
            if self.distance_behind_partner > self.security_distance > self.get_speed():
                slow_down = -1

        return slow_down

    def calc_distance_behind_partner(self):
        """
        calculates how far the distance the motorcyclist behind is. Has to be subtracted by oneto get actual distance
        :return:
        """
        if self.get_behind_partner() is not None:
            self.distance_behind_partner = (self.get_tile().get_index() -
                                            self.get_behind_partner().get_tile().get_index() - 1) % self.sim.length

    def calc_distance_ahead_partner(self):
        """
        calculates how far the distance the motorcyclist ahead is. Has to be subtracted by oneto get actual distance
        :return:
        """
        if self.get_ahead_partner() is not None:
            self.distance_ahead_partner = (self.get_ahead_partner().get_tile().get_index() -
                                           self.get_tile().get_index() - 1) % self.sim.length

    def update_partners(self):
        """
        updates the ahead and behind partners of the motorcyclist
        :return:
        """
        # order list of motorcyclists according to their position on the road
        self.my_platoon = sorted(self.my_platoon, key=lambda x: x.get_tile().get_index(), reverse=False)

        # update ahead and behind partners of all motorcyclists
        for i in range(len(self.my_platoon)):
            if i == 0:
                self.my_platoon[i].set_ahead_partner(self.my_platoon[i + 1])
                self.my_platoon[i].set_behind_partner(None)
            elif i == len(self.my_platoon) - 1:
                self.my_platoon[i].set_ahead_partner(None)
                self.my_platoon[i].set_behind_partner(self.my_platoon[i - 1])
            else:
                self.my_platoon[i].set_ahead_partner(self.my_platoon[i + 1])
                self.my_platoon[i].set_behind_partner(self.my_platoon[i - 1])

        self.update_role()
        self.calc_distance_behind_partner()
        self.calc_distance_ahead_partner()

    def update_role(self):
        """
        determines if the motorcyclist is a leader, sweeper or inbetween
        update_partners has to be called before
        :return:
        """
        if self.get_ahead_partner() is not None and self.get_behind_partner() is not None:
            self.is_inbetween = True
            self.is_leader = False
            self.is_sweeper = False
        elif self.get_ahead_partner() is not None:
            self.is_sweeper = True
            self.is_leader = False
            self.is_inbetween = False
        elif self.get_behind_partner() is not None:
            self.is_leader = True
            self.is_inbetween = False
            self.is_sweeper = False
        else:
            self.is_leader = False
            self.is_sweeper = False
            self.is_inbetween = False

    def check_switch_position(self):
        """
        returns a Boolean if Motorcyclist should switch lane. Will not switch lane if platoon member is directly ahead
        :return: Boolean to switch_lane
        """
        switch_lane = False

        self.look_at_positional_environment()
        self.update_partners()

        # asymmetric condition for switching lanes L->R see Rickert (T2-T4)
        if self.tile.get_lane() == 0:

            # cars always try to return to the right lane, independent of the situation on the left lane
            switch_lane = self.switch_possible()

            # do not switch lane if direct vehicle ahead is a platoon member. Shouldn't be too far away
            # Hint self.distance_front + 1 mandatory, since distance_front calculates the actual empty distance
            # the leader isn't affected since it has no partner ahead
            if self.distance_front < self.sim.get_length() / 10:
                vehicle = self.look_at_vehicle_at_pos(self.get_tile().get_index() + self.distance_front + 1,
                                                      self.tile.get_lane())
                if type(vehicle) is Motorcycle:
                    if vehicle.get_group() == self.get_group():
                        switch_lane = False

        # asymmetric condition for switching lanes R->L see Rickert (T1-T4)
        elif self.tile.get_lane() == 1:

            # current lane ahead has smaller space than current velocity + 1  security tile distance (T1)
            if self.distance_front < self.get_speed() + 1:
                switch_lane = self.switch_possible()

            # do not switch lane if direct vehicle ahead is a platoon member
            # Hint self.distance_front + 1 mandatory, since distance_front calculates the actual empty distance
            vehicle = self.look_at_vehicle_at_pos(self.get_tile().get_index() + self.distance_front + 1,
                                                  self.tile.get_lane())
            if type(vehicle) is Motorcycle:
                if vehicle.get_group() == self.get_group():
                    switch_lane = False

        return switch_lane

    def switch_possible(self):
        """
        returns a Boolean if Motorcyclist should switch lane. Instead, looking at maxV it looks at actual velocity
        :return:
        """
        switch = False

        if self.tile.get_lane() == 0:
            other_lane = 1
        elif self.tile.get_lane() == 1:
            other_lane = -1

        # switching only possible if side is free
        if self.sim.tiles[self.tile.get_index()][self.tile.get_lane() + other_lane].get_vehicle() is None:

            # Look what kind of vehicle is behind me
            look_street_idx = (self.tile.get_index() - self.distance_behind_other_lane - 1) % self.sim.length
            behind_vehicle_other_lane = self.look_at_vehicle_at_pos(look_street_idx, self.tile.get_lane() + other_lane)
            ahead_vehicle_other_lane = self.look_at_vehicle_at_pos(
                self.tile.get_index() + self.distance_front_other_lane + 1, self.tile.get_lane() + other_lane)

            # T2 more space than current velocity + 1
            if self.distance_front_other_lane > (self.get_speed() + 1):

                # motorcyclist takes actual velocity of the vehicle behind into account
                if behind_vehicle_other_lane is not None:
                    behind_speed = behind_vehicle_other_lane.get_speed()
                else:
                    behind_speed = 0

                # T3 more space than behind max_speed of rear car
                if self.distance_behind_other_lane > behind_speed:

                    # T4 random switch chance
                    if np.random.random() < self.sim.prob_changelane:
                        switch = True

            # if motorcyclist is on the left lane and on the right lane is a platoon member, switch lane
            elif self.get_tile().get_lane() == 0 and type(behind_vehicle_other_lane) is Motorcycle:
                if behind_vehicle_other_lane.get_group() == self.get_group():
                    # the behind_motorcyclist is not faster than the current motorcyclist
                    # if behind_vehicle.get_speed() <= self.get_speed():
                    if np.random.random() < self.sim.prob_changelane:
                        switch = True
            elif self.get_tile().get_lane() == 0 and type(ahead_vehicle_other_lane) is Motorcycle:
                if ahead_vehicle_other_lane.get_group() == self.get_group():
                    if np.random.random() < self.sim.prob_changelane:
                        switch = True

        return switch

    def set_behind_partner(self, partner):
        self.behind = partner

    def set_ahead_partner(self, partner):
        self.ahead = partner

    def set_my_platoon(self, platoon):
        self.my_platoon = platoon

    def set_symbol(self, symbol):
        self.symbol = symbol

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

    def get_role(self):
        if self.is_leader:
            return "leader"
        elif self.is_inbetween:
            return "inbetween"
        elif self.is_sweeper:
            return "sweeper"
        else:
            return "none"
