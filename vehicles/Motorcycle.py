from vehicles.Vehicles import *
import math


# --------------------------------------------------------------------------------------------------------------------
def normal_dist(diff, mean=0, sd=1, amp=1):
    """
    calculate value from normal distribution
    :param diff: the difference from optimal value
    :param amp: amplitude of NV to strengthen preference
    :param mean: mean of the preference normal distribution. usually zero
    :param sd: standard deviation of the preference normal distribution
    """
    var = float(sd) ** 2
    denominator = (2 * math.pi * var) ** .5
    num = math.exp(-(float(diff) - float(mean)) ** 2 / (2 * var))

    return amp * (num / denominator)


class Motorcycle(Vehicle):
    # max_velocity: 100km/h = 30m/s -> 30m/s / 3,75m = 8tiles
    def __init__(self, speed, tile, group, preferred_speed, speed_distance_preferences=None, max_velocity=8):
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
        self.is_lost = False

        # optimal distance in last step achieved
        self.behind_optimal_distance = False
        self.front_optimal_distance = False

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
            if self.distance_front > self.get_speed() + self.speed_up() and \
                    self.get_speed() + self.speed_up() < self.get_maxV() and \
                    self.get_speed() + self.speed_up() < self.get_tile().get_speed_limit():
                self.set_speed(self.get_speed() + self.speed_up() + 1)

            else:
                self.set_speed(self.get_speed() + 1)

        # 2. slowdown if too far from behind partner
        # in case of first and second if statement are true, then offset initial catch_up speed
        if self.get_behind_partner() is not None:
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

    def update_speed_with_preference(self):
        """
        all motorcyclist have the same set of rules
        :return:
        """
        self.look_at_positional_environment()
        self.update_partners()
        self.update_preferences(self.tile.get_curvature())

        close_up_dist_behind = self.estimate_close_up_distance_partner('behind')
        close_up_dist_ahead = self.estimate_close_up_distance_partner('ahead')

        changed_speed = False

        if self.tile.get_lane() == 0:
            other_lane = 1
        elif self.tile.get_lane() == 1:
            other_lane = -1

        # Look what kind of vehicle around me
        idx_behind = (self.tile.get_index() - self.distance_behind - 1) % self.sim.get_length()
        idx_ahead = (self.tile.get_index() + self.distance_front + 1) % self.sim.get_length()
        behind_vehicle = self.look_at_vehicle_at_pos(idx_behind, self.get_tile().get_lane())
        ahead_vehicle = self.look_at_vehicle_at_pos(idx_ahead, self.tile.get_lane())

        idx_behind_other = (self.tile.get_index() - self.distance_behind_other_lane - 1) % self.sim.get_length()
        idx_ahead_other = (self.tile.get_index() + self.distance_front_other_lane + 1) % self.sim.get_length()
        behind_vehicle_other_lane = self.look_at_vehicle_at_pos(idx_behind_other, self.tile.get_lane() + other_lane)
        ahead_vehicle_other_lane = self.look_at_vehicle_at_pos(idx_ahead_other, self.tile.get_lane() + other_lane)

        ahead_partner_in_sight = False
        behind_partner_in_sight = False
        if ahead_vehicle is self.get_ahead_partner() or ahead_vehicle_other_lane is self.get_ahead_partner():
            if ahead_vehicle is not None:
                if ahead_vehicle.get_role() != 'sweeper':
                    ahead_partner_in_sight = True
            if ahead_vehicle_other_lane is not None:
                if ahead_vehicle_other_lane.get_role() != 'sweeper':
                    ahead_partner_in_sight = True
        if behind_vehicle is self.get_behind_partner() or behind_vehicle_other_lane is self.get_behind_partner():
            if behind_vehicle is not None:
                if behind_vehicle.get_role() != 'leader':
                    behind_partner_in_sight = True
                if behind_vehicle_other_lane is not None:
                    if behind_vehicle_other_lane.get_role() != 'leader':
                        behind_partner_in_sight = True

        # 1. adjust speed to get optimal distance to behind partner
        if behind_partner_in_sight or self.get_role() == 'sweeper':
            # decelerate if too close to behind partner. But be faster than a Bike
            if close_up_dist_behind > self.behind_gap_preference and self.get_speed() > 2:
                self.set_speed(self.get_speed() - 1)
                changed_speed = True
            # accelerate if too far from behind partner
            elif close_up_dist_behind < self.behind_gap_preference:
                self.set_speed(self.get_speed() + 1)
                changed_speed = True

        # 2. adjust speed to get optimal distance to ahead partner
        if ahead_partner_in_sight and not changed_speed:
            # decelerate if too close to ahead partner
            if close_up_dist_ahead > self.front_gap_preference:
                self.set_speed(self.get_speed() + 1)
            # accelerate if too far from ahead partner
            elif close_up_dist_ahead < self.front_gap_preference:
                self.set_speed(self.get_speed() - 1)
            # adjust speed to preference
            # elif close_up_dist_ahead == self.front_gap_preference:
            #     if self.get_speed() < self.current_speed_preference:
            #         self.set_speed(self.get_speed() + 1)
            #     elif self.get_speed() > self.current_speed_preference:
            #        self.set_speed(self.get_speed() - 1)
            #    else:
            #        # everything optimal
            #        pass

        # 3. if optimal distance behind achieved
        if close_up_dist_behind == self.behind_gap_preference and not changed_speed:
            if self.get_speed() < self.current_speed_preference:
                self.set_speed(self.get_speed() + 1)
            elif self.get_speed() > self.current_speed_preference:
                self.set_speed(self.get_speed() - 1)
            else:
                # everything optimal
                pass
        else:
            # adjust speed to preference
            if close_up_dist_ahead == self.front_gap_preference and not changed_speed:
                if self.get_speed() < self.current_speed_preference:
                    self.set_speed(self.get_speed() + 1)
                elif self.get_speed() > self.current_speed_preference:
                    self.set_speed(self.get_speed() - 1)
                else:
                    # everything optimal
                    pass

        # 4. if neither is in direct sight, then adjust speed to preference meaning the biker is lost
        if not ahead_partner_in_sight and not behind_partner_in_sight:
            if self.get_speed() < self.current_speed_preference:
                self.set_speed(self.get_speed() + 1)
            elif self.get_speed() > self.current_speed_preference:
                self.set_speed(self.get_speed() - 1)
            else:
                # optimal speed
                pass

        # todo adjust speed for more cases
        # 5. if motorcyclist is on the left lane he wants to overtake the slower vehicle on the right lane
        if self.tile.get_lane() == 0 and ahead_vehicle_other_lane is not None:
            idx = ahead_vehicle_other_lane.get_tile().get_index()
            lane = ahead_vehicle_other_lane.get_tile().get_lane()
            # vehicle can be overtaken since it is slower than the motorcyclist
            if self.estimate_close_up_distance(idx, lane) < 0:
                self.set_speed(self.get_speed() + 1)
            else:
                # hold the current speed according to other rules and abort overtaking
                pass

        # general_speed_adjustments for all scenarios
        # 0. Cannot drive backwards
        if self.get_speed() < 0:
            self.set_speed(0)

        # 1. Cannot be faster than motorcycle max speed
        if self.get_speed() > self.get_maxV():
            self.set_speed(self.get_maxV())

        # 2. Slowing down with no tile security distance. No security distance
        if self.distance_front <= self.get_speed():
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

        self.calculate_fun()

    # todo delete
    def update_speed_with_preferenceV5(self):
        """
        first the leader adjust its distance. All other motorcyclist adjust to the ahead partner distance
        :return:
        """
        self.look_at_positional_environment()
        self.update_partners()
        self.update_preferences(self.tile.get_curvature())

        close_up_dist_behind = self.estimate_close_up_distance_partner('behind')
        close_up_dist_ahead = self.estimate_close_up_distance_partner('ahead')

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

        peak = self.estimate_close_up_distance_partner(self.tile.get_curvature())
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
                overall_gap_distance += self.estimate_close_up_distance_partner('behind')
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
    def estimate_close_up_distance_partner(self, partner):
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
        elif self.get_ahead_partner() is None:
            close_up_dist = self.front_gap_preference
        elif self.get_behind_partner() is None:
            close_up_dist = self.behind_gap_preference
        else:
            # if self is leader he does not have a partner ahead. if self is sweeper he does not have a partner behind
            pass

        return close_up_dist

    def estimate_close_up_distance(self, idx, lane):
        """
        estimated distance to the vehicle in front or other lane at idx tile to itself
        :param lane: the lane position of the vehicle in question
        :param idx: idx of the vehicle
        :return: estimated distance to the vehicle. Positive means the vehicle will be further away. Negative means the
        vehicle can be overtaken
        """
        vehicle = self.look_at_vehicle_at_pos(idx, lane)
        dist_diff = -1
        if vehicle is not None:
            if vehicle.get_moved():
                dist_diff = (idx - self.get_tile().get_index() - self.get_speed()) % self.sim.get_length()
            else:
                dist_diff = (
                                    idx - self.get_tile().get_index() + vehicle.get_speed() - self.get_speed()) % self.sim.get_length()
        return dist_diff

    def estimate_catch_up_distance(self, idx, lane):
        """
        estimated distance to the vehicle behind or other lane at idx tile to itself
        :param idx: idx of the vehicle
        :param lane: lane position of the vehicle
        :return: estimated distance to the vehicle. Positive means the vehicle cannot overtake us. Negative it can
        """
        vehicle = self.look_at_vehicle_at_pos(idx, lane)
        dist_diff = 1
        if vehicle is not None:
            if vehicle.get_moved():
                dist_diff = (self.get_tile().get_index() - idx + self.get_speed()) % self.sim.get_length()
            else:
                dist_diff = (self.get_tile().get_index() - idx - vehicle.get_speed() + self.get_speed()) % self.sim.get_length()
        return dist_diff

    def speed_up(self):
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

    def slow_down_to_behind_partner(self):
        """
        extra slow_down to behind partner if behind partner is too far away
        :return: -1 if too far away else 0
        """
        slow_down = 0
        if self.get_behind_partner() is not None:
            if self.distance_behind_partner + 1 > self.behind_gap_preference:
                slow_down = -1

        return slow_down

    def speed_up_to_ahead_partner(self):
        """
        extra speed_up to ahead partner if ahead partner is too far away
        :return: 1 if too far away else 0
        """
        speed_up = 0
        if self.get_ahead_partner() is not None:
            if self.distance_ahead_partner - 1 < self.front_gap_preference:
                speed_up = 1

        return speed_up

    def calc_distance_behind_partner(self):
        """
        calculates how far the distance the motorcyclist behind is. Has to be subtracted by oneto get actual distance
        :return:
        """
        '''
        if self.get_behind_partner() is not None:
            self.distance_behind_partner = (self.get_tile().get_index() -
                                            self.get_behind_partner().get_tile().get_index() - 1) % self.sim.length
        '''
        if self.get_behind_partner() is not None:
            self.distance_behind_partner = (abs(self.get_tile().get_index() -
                                            self.get_behind_partner().get_tile().get_index() - 1))
        else:
            # if there is no behind partner than the optimal length distance if always achieved
            self.distance_behind_partner = self.behind_gap_preference

    def calc_distance_ahead_partner(self):
        """
        calculates how far the distance the motorcyclist ahead is. Has to be subtracted by oneto get actual distance
        :return:
        """
        if self.get_ahead_partner() is not None:
            self.distance_ahead_partner = (abs(self.get_ahead_partner().get_tile().get_index() -
                                           self.get_tile().get_index() - 1))
        else:
            # if there is no ahead partner than the optimal length distance if always achieved
            self.distance_ahead_partner = self.front_gap_preference

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
                if self.my_platoon[i].get_tile().get_index() == self.my_platoon[i + 1].get_tile().get_index():
                    # same tile index but one is on the right lane
                    if self.my_platoon[i].get_tile().get_lane() > self.my_platoon[i + 1].get_tile().get_lane():
                        self.my_platoon[i + 1].set_behind_partner(self.my_platoon[i])
                        self.my_platoon[i].set_ahead_partner(self.my_platoon[i + 1])
                        self.my_platoon[i].set_behind_partner(None)
                    else:
                        self.my_platoon[i].set_behind_partner(self.my_platoon[i + 1])
                        self.my_platoon[i + 1].set_ahead_partner(self.my_platoon[i])
                        self.my_platoon[i + 1].set_behind_partner(None)
                else:
                    self.my_platoon[i].set_ahead_partner(self.my_platoon[i + 1])
                    self.my_platoon[i + 1].set_behind_partner(self.my_platoon[i])
                    self.my_platoon[i].set_behind_partner(None)

            elif i == len(self.my_platoon) - 1:
                if self.my_platoon[i].get_tile().get_index() == self.my_platoon[i - 1].get_tile().get_index():
                    # same tile index but one is on the right lane
                    if self.my_platoon[i].get_tile().get_lane() > self.my_platoon[i - 1].get_tile().get_lane():
                        self.my_platoon[i - 1].set_behind_partner(self.my_platoon[i])
                        self.my_platoon[i].set_ahead_partner(self.my_platoon[i - 1])
                        self.my_platoon[i - 1].set_ahead_partner(None)
                    else:
                        self.my_platoon[i].set_behind_partner(self.my_platoon[i - 1])
                        self.my_platoon[i - 1].set_ahead_partner(self.my_platoon[i])
                        self.my_platoon[i].set_ahead_partner(None)
                else:
                    self.my_platoon[i].set_ahead_partner(None)
                    self.my_platoon[i].set_behind_partner(self.my_platoon[i - 1])
            else:
                if self.my_platoon[i].get_tile().get_index() == self.my_platoon[i + 1].get_tile().get_index():
                    if self.my_platoon[i].get_tile().get_lane() > self.my_platoon[i + 1].get_tile().get_lane():
                        self.my_platoon[i + 1].set_behind_partner(self.my_platoon[i])
                        self.my_platoon[i].set_ahead_partner(self.my_platoon[i + 1])
                    else:
                        self.my_platoon[i].set_behind_partner(self.my_platoon[i + 1])
                        self.my_platoon[i + 1].set_ahead_partner(self.my_platoon[i])
                else:
                    self.my_platoon[i].set_ahead_partner(self.my_platoon[i + 1])
                    self.my_platoon[i + 1].set_behind_partner(self.my_platoon[i])

        self.update_role()
        self.check_roles()
        self.calc_distance_behind_partner()
        self.calc_distance_ahead_partner()

    def update_role(self):
        """
        determines if the motorcyclist is a leader, sweeper or inbetween
        update_partners has to be called before
        :return:
        """
        for motorcyclist in self.my_platoon:
            if motorcyclist.get_ahead_partner() is not None and motorcyclist.get_behind_partner() is not None:
                motorcyclist.set_role("inbetween")
            elif motorcyclist.get_behind_partner() is None:
                motorcyclist.set_role("sweeper")
            elif motorcyclist.get_ahead_partner() is None:
                motorcyclist.set_role("leader")
            elif motorcyclist.get_ahead_partner() is None and motorcyclist.get_behind_partner() is None:
                motorcyclist.set_role("lost")

    def check_roles(self):
        """
        check the roles. There should be always and only one leader and sweeper the rest are inbetween
        :return:
        """
        leader = 0
        sweeper = 0
        inbetween = 0
        for m in self.my_platoon:
            if m.is_leader:
                leader += 1
            elif m.is_sweeper:
                sweeper += 1
            elif m.is_inbetween:
                inbetween += 1
        if leader != 1 or sweeper != 1 or inbetween != len(self.my_platoon) - 2:
            print('#leader, #sweeper, #inbetween: ', leader, sweeper, inbetween)
            raise Exception("Roles are not correct")

    def check_switch_position(self):
        """
        returns a Boolean if Motorcyclist should switch lane. Will not switch lane if platoon member is directly ahead
        :return: Boolean to switch_lane
        """
        switch_lane = False

        self.look_at_positional_environment()
        self.update_partners()

        idx_ahead = (self.tile.get_index() + self.distance_front + 1) % self.sim.get_length()
        ahead_vehicle = self.look_at_vehicle_at_pos(idx_ahead, self.tile.get_lane())

        # asymmetric condition for switching lanes L->R see Rickert (T2-T4)
        if self.tile.get_lane() == 0:

            # cars always try to return to the right lane, independent of the situation on the left lane
            switch_lane = self.switch_possible()

            # do not switch lane if direct vehicle ahead is a platoon member. Shouldn't be too far away
            # Hint self.distance_front + 1 mandatory, since distance_front calculates the actual empty distance
            # Hint the leader isn't affected since it has no partner ahead
            if self.distance_front < self.sim.get_length() / 10:
                if type(ahead_vehicle) is Motorcycle:
                    if ahead_vehicle.get_group() == self.get_group() or ahead_vehicle.get_role() == "sweeper":
                        switch_lane = False

        # asymmetric condition for switching lanes R->L see Rickert (T1-T4)
        elif self.tile.get_lane() == 1:

            # current lane ahead has smaller space than 2 * current velocity + 1 security tile distance (T1)
            if self.distance_front < 2 * self.get_speed() + 1:
                switch_lane = self.switch_possible()

            # do not switch lane if direct vehicle ahead is a platoon member
            if type(ahead_vehicle) is Motorcycle:
                if ahead_vehicle.get_group() == self.get_group() or ahead_vehicle.get_role() == "sweeper":
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

            # Look what kind of vehicle around me
            idx_behind = (self.tile.get_index() - self.distance_behind - 1) % self.sim.get_length()
            idx_ahead = (self.tile.get_index() + self.distance_front + 1) % self.sim.get_length()
            behind_vehicle = self.look_at_vehicle_at_pos(idx_behind, self.get_tile().get_lane())
            ahead_vehicle = self.look_at_vehicle_at_pos(idx_ahead, self.tile.get_lane())

            idx_behind_other = (self.tile.get_index() - self.distance_behind_other_lane - 1) % self.sim.get_length()
            idx_ahead_other = (self.tile.get_index() + self.distance_front_other_lane + 1) % self.sim.get_length()

            behind_vehicle_other_lane = self.look_at_vehicle_at_pos(idx_behind_other, self.tile.get_lane() + other_lane)
            ahead_vehicle_other_lane = self.look_at_vehicle_at_pos(idx_ahead_other, self.tile.get_lane() + other_lane)

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

            # if motorcyclist is on the right lane and on the left lane front is a platoon member
            elif type(ahead_vehicle_other_lane) is Motorcycle:
                if ahead_vehicle_other_lane.get_group() == self.get_group() and ahead_vehicle_other_lane.get_role() != "sweeper":
                    if np.random.random() < self.sim.prob_changelane:
                        switch = True

            elif self.get_tile().get_lane() == 1 and type(behind_vehicle_other_lane) is Motorcycle:
                if behind_vehicle_other_lane.get_group() == self.get_group() and behind_vehicle_other_lane.get_role() != "sweeper":
                    if np.random.random() < self.sim.prob_changelane:
                        switch = True

        # todo delete
        if self.get_role() == "leader":
            if self.get_tile().get_lane() == 1:
                if switch == True:
                    pass

        return switch

    def calculate_fun(self):
        """
        calculates the fun. Fun depends on actual distance to partners on distance preference and speed preference
        speed is weighted according to curvature. See curve_fun_preference in config.py
        Reminder: motorcyclist only see the actual index of the ahead_partner in the current turn. Thus cannot
        see itself the updated index nor the updated index of the behind_partner
        :return:
        """
        gain_ahead = 0
        gain_behind = 0
        gain_speed = 0

        if self.get_role() == "inbetween":
            diff_ahead_partner = abs(self.distance_ahead_partner - self.front_gap_preference - self.get_speed())
            diff_behind_partner = abs(self.distance_behind_partner - self.behind_gap_preference)
            diff_speed = abs(self.get_speed() - self.current_speed_preference)

            gain_ahead = normal_dist(diff_ahead_partner, mean=0, sd=1, amp=self.front_gap_ampl)
            gain_behind = normal_dist(diff_behind_partner, mean=0, sd=1, amp=self.behind_gap_ampl)
            gain_speed = normal_dist(diff_speed, mean=0, sd=1, amp=self.speed_ampl)

        elif self.get_role() == 'leader':
            diff_behind_partner = abs(self.distance_behind_partner - self.behind_gap_preference)
            diff_speed = abs(self.get_speed() - self.current_speed_preference)

            gain_behind = normal_dist(diff_behind_partner, mean=0, sd=1, amp=self.behind_gap_ampl)
            gain_ahead = gain_behind
            gain_speed = normal_dist(diff_speed, mean=0, sd=1, amp=self.speed_ampl)

        elif self.get_role() == 'sweeper':
            diff_ahead_partner = abs(self.distance_ahead_partner - self.front_gap_preference - self.get_speed())
            diff_speed = abs(self.get_speed() - self.current_speed_preference)

            gain_ahead = normal_dist(diff_ahead_partner, mean=0, sd=1, amp=self.front_gap_ampl)
            gain_behind = gain_ahead
            gain_speed = normal_dist(diff_speed, mean=0, sd=1, amp=self.speed_ampl)

        self.fun = gain_ahead + gain_behind + self.fun_weight * gain_speed

    def set_behind_partner(self, partner):
        self.behind = partner

    def set_ahead_partner(self, partner):
        self.ahead = partner

    def set_my_platoon(self, platoon):
        self.my_platoon = platoon

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_role(self, role):
        if role == 'leader':
            self.is_leader = True
            self.is_inbetween = False
            self.is_sweeper = False
        elif role == 'inbetween':
            self.is_leader = False
            self.is_inbetween = True
            self.is_sweeper = False
        elif role == 'sweeper':
            self.is_leader = False
            self.is_inbetween = False
            self.is_sweeper = True
        elif role == 'lost':
            self.is_leader = False
            self.is_inbetween = False
            self.is_sweeper = False

    def set_moved(self, moved=False):
        """
        last function call for this cycle
        :param moved:
        :return:
        """
        self.moved = moved

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
        elif self.is_lost:
            return "lost"

    def get_fun(self):
        return self.fun
