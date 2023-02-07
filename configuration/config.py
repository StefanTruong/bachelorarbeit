import numpy as np


class ConfigPreference:
    selection_1 = {
        'length': 40,  # don't use more than 50 for visualization as console cannot display more at once
        'total_amount_steps': 10,
        'density': 0.5,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': -1,
        'prob_changelane': 1,
        'car_share': 0.9,
        'number_platoons': 3,
        'platoon_size': 3,
        'car_max_velocity': 10,
        'bike_max_velocity': 2,
        'motorcycle_max_velocity': 7,
        'speed_preferences': ['cautious', 'average', 'speed'],
        # available distance_preferences one-sided or behind_ahead
        'distance_preferences': ['small', 'avg', 'high',
                                 'small_small', 'small_avg', 'small_high', 'avg_avg', 'avg_high',
                                 'high_high', 'high_small', 'high_avg', 'avg_small'],
        'speed_distance_preferences': {
            'cautious': {'behind_gap_preference': 'high',
                         'front_gap_preference': 'high',
                         'inbetween_gap_preference': 'high_high'},
            'average': {'behind_gap_preference': 'avg',
                        'front_gap_preference': 'avg',
                        'inbetween_gap_preference': 'avg_avg'},
            'speed': {'behind_gap_preference': 'small',
                      'front_gap_preference': 'small',
                      'inbetween_gap_preference': 'small_small'},
        },
        'biker_composition_modus': 'equal',
        'adjust_speed_preference': False}
    selection_2 = {
        'length': 20,  # don't use more than 50 for visualization as console cannot display more at once
        'total_amount_steps': 100,
        'density': 1,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.1,
        'prob_changelane': 0.5,
        'car_share': 0.9,
        'number_platoons': 3,
        'platoon_size': 3,
        'car_max_velocity': 10,
        'bike_max_velocity': 2,
        'motorcycle_max_velocity': 7,
        'speed_preferences': ['cautious', 'average', 'speed'],
        # available distance_preferences one-sided or behind_ahead
        'distance_preferences': ['small', 'avg', 'high',
                                 'small_small', 'small_avg', 'small_high', 'avg_avg', 'avg_high',
                                 'high_high', 'high_small', 'high_avg', 'avg_small'],
        'speed_distance_preferences': {
            'cautious': {'behind_gap_preference': 'high',
                         'front_gap_preference': 'high',
                         'inbetween_gap_preference': 'high_high'},
            'average': {'behind_gap_preference': 'avg',
                        'front_gap_preference': 'avg',
                        'inbetween_gap_preference': 'avg_avg'},
            'speed': {'behind_gap_preference': 'small',
                      'front_gap_preference': 'small',
                      'inbetween_gap_preference': 'small_small'},
        },
        'biker_composition_modus': 'equal',
        'adjust_speed_preference': False}
    selection_3 = {
        'length': 50,  # don't use more than 50 for visualization as console cannot display more at once
        'total_amount_steps': 100,
        'density': 0.5,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': -1,
        'prob_changelane': 1,
        'car_share': 0.9,
        'number_platoons': 1,
        'platoon_size': 1,
        'car_max_velocity': 10,
        'bike_max_velocity': 2,
        'motorcycle_max_velocity': 7,
        'speed_preferences': ['cautious', 'average', 'speed'],
        # available distance_preferences one-sided or behind_ahead
        'distance_preferences': ['small', 'avg', 'high',
                                 'small_small', 'small_avg', 'small_high', 'avg_avg', 'avg_high',
                                 'high_high', 'high_small', 'high_avg', 'avg_small'],
        'speed_distance_preferences': {
            'cautious': {'behind_gap_preference': 'high',
                         'front_gap_preference': 'high',
                         'inbetween_gap_preference': 'high_high'},
            'average': {'behind_gap_preference': 'avg',
                        'front_gap_preference': 'avg',
                        'inbetween_gap_preference': 'avg_avg'},
            'speed': {'behind_gap_preference': 'small',
                      'front_gap_preference': 'small',
                      'inbetween_gap_preference': 'small_small'},
        },
        'biker_composition_modus': 'equal',
        'adjust_speed_preference': False}
    selection_4 = {
        'length': 40,  # don't use more than 50 for visualization as console cannot display more at once
        'total_amount_steps': 100,
        'density': 2,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.2,
        'prob_changelane': 0.5,
        'car_share': 0.9,
        'number_platoons': 1,
        'platoon_size': 3,
        'car_max_velocity': 10,
        'bike_max_velocity': 2,
        'motorcycle_max_velocity': 7,
        'speed_preferences': ['cautious', 'average', 'speed'],
        # available distance_preferences one-sided or behind_ahead
        'distance_preferences': ['small', 'avg', 'high',
                                 'small_small', 'small_avg', 'small_high', 'avg_avg', 'avg_high',
                                 'high_high', 'high_small', 'high_avg', 'avg_small'],
        'speed_distance_preferences': {
            'cautious': {'behind_gap_preference': 'high',
                         'front_gap_preference': 'high',
                         'inbetween_gap_preference': 'high_high'},
            'average': {'behind_gap_preference': 'avg',
                        'front_gap_preference': 'avg',
                        'inbetween_gap_preference': 'avg_avg'},
            'speed': {'behind_gap_preference': 'small',
                      'front_gap_preference': 'small',
                      'inbetween_gap_preference': 'small_small'},
        },
        'biker_composition_modus': 'equal',
        'adjust_speed_preference': False}
    selection_5 = {
        'length': 100,  # don't use more than 50 for visualization as console cannot display more at once
        'total_amount_steps': 100,
        'density': 0.2,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.2,
        'prob_changelane': 0.5,
        'car_share': 0.9,
        'number_platoons': 3,
        'platoon_size': 3,
        'car_max_velocity': 10,
        'bike_max_velocity': 2,
        'motorcycle_max_velocity': 7,
        'speed_preferences': ['cautious', 'average', 'speed'],
        # available distance_preferences one-sided or behind_ahead
        'distance_preferences': ['small', 'avg', 'high',
                                 'small_small', 'small_avg', 'small_high', 'avg_avg', 'avg_high',
                                 'high_high', 'high_small', 'high_avg', 'avg_small'],
        'speed_distance_preferences': {
            'cautious': {'behind_gap_preference': 'high',
                         'front_gap_preference': 'high',
                         'inbetween_gap_preference': 'high_high'},
            'average': {'behind_gap_preference': 'avg',
                        'front_gap_preference': 'avg',
                        'inbetween_gap_preference': 'avg_avg'},
            'speed': {'behind_gap_preference': 'small',
                      'front_gap_preference': 'small',
                      'inbetween_gap_preference': 'small_small'},
        },
        'biker_composition_modus': 'equal',
        'adjust_speed_preference': False}
    selection_6 = {
        'length': 100,  # don't use more than 50 for visualization as console cannot display more at once
        'total_amount_steps': 100,
        'density': 0.2,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.2,
        'prob_changelane': 0.5,
        'car_share': 0.9,
        'number_platoons': 3,
        'platoon_size': 3,
        'car_max_velocity': 10,
        'bike_max_velocity': 2,
        'motorcycle_max_velocity': 7,
        'speed_preferences': ['cautious', 'average', 'speed'],
        # available distance_preferences one-sided or behind_ahead
        'distance_preferences': ['small', 'avg', 'high',
                                 'small_small', 'small_avg', 'small_high', 'avg_avg', 'avg_high',
                                 'high_high', 'high_small', 'high_avg', 'avg_small'],
        'speed_distance_preferences': {
            'cautious': {'behind_gap_preference': 'high',
                         'front_gap_preference': 'high',
                         'inbetween_gap_preference': 'high_high'},
            'average': {'behind_gap_preference': 'avg',
                        'front_gap_preference': 'avg',
                        'inbetween_gap_preference': 'avg_avg'},
            'speed': {'behind_gap_preference': 'small',
                      'front_gap_preference': 'small',
                      'inbetween_gap_preference': 'small_small'},
        },
        'biker_composition_modus': 'equal',
        'adjust_speed_preference': False}
    selection_7 = {
        'length': 30,  # don't use more than 50 for visualization as console cannot display more at once
        'total_amount_steps': 100,
        'density': 0.5,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.1,
        'prob_changelane': 0.2,
        'car_share': 0.9,
        'number_platoons': 1,
        'platoon_size': 3,
        'car_max_velocity': 10,
        'bike_max_velocity': 2,
        'motorcycle_max_velocity': 7,
        'speed_preferences': ['cautious', 'average', 'speed'],
        # available distance_preferences one-sided or behind_ahead
        'distance_preferences': ['small', 'avg', 'high',
                                 'small_small', 'small_avg', 'small_high', 'avg_avg', 'avg_high',
                                 'high_high', 'high_small', 'high_avg', 'avg_small'],
        'speed_distance_preferences': {
            'cautious': {'behind_gap_preference': 'high',
                         'front_gap_preference': 'high',
                         'inbetween_gap_preference': 'high_high'},
            'average': {'behind_gap_preference': 'avg',
                        'front_gap_preference': 'avg',
                        'inbetween_gap_preference': 'avg_avg'},
            'speed': {'behind_gap_preference': 'small',
                      'front_gap_preference': 'small',
                      'inbetween_gap_preference': 'small_small'},
        },
        'biker_composition_modus': 'equal',
        'adjust_speed_preference': False}
    selection_8 = {
        'length': 1000,  # don't use more than 50 for visualization as console cannot display more at once
        'total_amount_steps': 100,
        'density': 0.1,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.1,
        'prob_changelane': 0.2,
        'car_share': 1,
        'number_platoons': 1,
        'platoon_size': 4,
        'car_max_velocity': 10,
        'bike_max_velocity': 2,
        'motorcycle_max_velocity': 7,
        'speed_preferences': ['cautious', 'average', 'speed'],
        # available distance_preferences one-sided or behind_ahead
        'distance_preferences': ['small', 'avg', 'high',
                                 'small_small', 'small_avg', 'small_high', 'avg_avg', 'avg_high',
                                 'high_high', 'high_small', 'high_avg', 'avg_small'],
        'speed_distance_preferences': {
            'cautious': {'behind_gap_preference': 'high',
                         'front_gap_preference': 'high',
                         'inbetween_gap_preference': 'high_high'},
            'average': {'behind_gap_preference': 'avg',
                        'front_gap_preference': 'avg',
                        'inbetween_gap_preference': 'avg_avg'},
            'speed': {'behind_gap_preference': 'small',
                      'front_gap_preference': 'small',
                      'inbetween_gap_preference': 'small_small'},
        },
        'biker_composition_modus': 'equal',
        'adjust_speed_preference': False}
    selection_9 = None

    def __init__(self, configuration=None):
        if configuration is None or configuration == 'default':
            # # model settings
            """
            initializing model parameters
            :param length: length of the trip in tiles. Size of the array. Begins with index 0
            :param density: length*density == #total number of vehicles. Value between [0,2]
            :param prob_slowdown: chance of slowing down. Value between [0,1]
            :param num_lanes: begins with index 0 for left lane. Currently works only exactly for 2 lanes!
            :param prob_changelane: probability changing_lane L->R for overtaking
            :param car_share: [0,1]
            :param number_platoons: has to be lower than total number of total vehicles
            :param platoon_size: has to be greater than 1
            :param total_amount_steps: determines how many steps the simulation stops
            :param speed_preferences: available speed preferences: 'speed', 'average', 'cautious'
            :param speed_distance_prereferences: matching speed preferences with distance preferences
            :param biker_composition_modus: how the preference distribution of bikers is generated
                    equal:  equal distribution of speed_preferences in the platoon
                            Beginning with cautious first, then average and then speed
                    average_only: only average speed preference in the platoon
                    cautious_only: only cautious speed preference in the platoon
                    speed_only: only speed speed preference in the platoon
            :param adjust_speed_preference: when Motorcyclist should update its speed according to its speed-gap pref
            """
            self.model_settings = {
                'length': 2000,
                'total_amount_steps': 200,
                'density': 0.0025,
                'num_lanes': 1,  # [0,1] do not change
                'prob_slowdown': 0.00,  # should be turned off as Motorcyclist behave irregularly
                'prob_changelane': 0.99,
                'car_share': 1.0,
                'number_platoons': 1,
                'platoon_size': 5,
                'car_max_velocity': 11,  # 120[km/h] = 33.33[m/s] ~ 33/3 = 11
                'bike_max_velocity': 2,  # 20[km/h] = 5.56[m/s] ~ 5/3 = 1.67
                'motorcycle_max_velocity': 9,  # 100[km/h] = 27.78[m/s] ~ 27/3 = 9
                'speed_preferences': ['cautious', 'average', 'speed'],
                # available distance_preferences one-sided or behind_ahead
                'distance_preferences': ['small', 'avg', 'high',
                                         'small_small', 'small_avg', 'small_high', 'avg_avg', 'avg_high',
                                         'high_high', 'high_small', 'high_avg', 'avg_small'],
                'speed_distance_preferences': {
                    'cautious': {'behind_gap_preference': 'high',
                                 'front_gap_preference': 'high',
                                 'inbetween_gap_preference': 'high_high'},
                    'average': {'behind_gap_preference': 'avg',
                                'front_gap_preference': 'avg',
                                'inbetween_gap_preference': 'avg_avg'},
                    'speed': {'behind_gap_preference': 'small',
                              'front_gap_preference': 'small',
                              'inbetween_gap_preference': 'small_small'},
                },
                'biker_composition_modus': 'average_only',
                'adjust_speed_preference': True
            }
        elif configuration == 'selection_1':
            self.model_settings = self.selection_1
        elif configuration == 'selection_2':
            self.model_settings = self.selection_2
        elif configuration == 'selection_3':
            self.model_settings = self.selection_3
        elif configuration == 'selection_4':
            self.model_settings = self.selection_4
        elif configuration == 'selection_5':
            self.model_settings = self.selection_5
        elif configuration == 'selection_6':
            self.model_settings = self.selection_6
        elif configuration == 'selection_7':
            self.model_settings = self.selection_7
        elif configuration == 'selection_8':
            self.model_settings = self.selection_8
        else:
            raise ValueError('Unknown configuration')

        # # curve-speed-limit
        # don't forget to adjust the symbol in tile.py for the curvature
        self.speedlimit_to_curvature = {
            11: (0, 200),  # 7 tiles ~ 28 m/s ~ 101 km/h
            8: (200, 500),  # 6 tiles ~ 24 m/s ~ 86 km/h
            7: (500, 900),  # 5 tiles ~ 20 m/s ~ 72 km/h
            6: (900, 1200),  # 4 tiles ~ 16 m/s ~ 57 km/h
            5: (1200, 1500),  # 3 tiles ~ 12 m/s ~ 43 km/h
            4: (1500, 1900),  # 2 tiles ~ 8 m/s ~ 29 km/h
            3: (1900, 10000),  # 1 tile ~ 4 m/s ~ 14 km/h
        }

        # # Preference Settings
        # distance preference single sided
        self.dist_mean_small = 2  # 50[km/h] ~ 13[m/s]*2[sec] / 4[m/tile] ~ 3[tiles]
        self.dist_sd_small = 1
        self.dist_ampl_small = 1
        self.dist_mean_avg = 5  # see: https://www.mcuckermark.de/wp-content/uploads/2019/07/Fahren-in-einer-Motorradgruppe.pdf
        self.dist_sd_avg = 1
        self.dist_ampl_avg = 1
        self.dist_mean_high = 4
        self.dist_sd_high = 1
        self.dist_ampl_high = 1

        # curve speed preference
        self.curve_preference_cautious = None
        self.curve_preference_average = None
        self.curve_preference_speed = None
        self.curve_sd_cautious = 1
        self.curve_ampl_cautious = 1
        self.curve_sd_average = 1
        self.curve_ampl_average = 1
        self.curve_sd_speed = 1
        self.curve_ampl_speed = 1

        # How far the NV should be calculated. Length of data has to match with length for pdf and gradient to match
        self.dist_preference_sight = np.linspace(0, 50, 50)

        # The speed type wants to ride maximum speed
        self.curve_preference_speed = self.speedlimit_to_curvature

        # The average type wants to ride roughly one speed less
        self.curve_preference_average = {
            8: (0, 200),
            7: (200, 500),
            6: (500, 900),
            5: (900, 1200),
            4: (1200, 1500),
            3: (1500, 1900),
            2: (1900, 10000),
        }

        # The cautious type wants to ride roughly two speed less
        self.curve_preference_cautious = {
            7: (0, 200),
            6: (200, 500),
            5: (500, 900),
            4: (900, 1200),
            3: (1200, 1500),
            2: (1500, 1900),
            1: (1900, 10000),
        }

        # more curvature more fun. Keys [0,1] in relation to distance preference
        self.curve_fun_preference = {
            0.25: (0, 400),
            1: (400, 10000),
        }

    # ToDo check if this works
    def get_distance_preference(self, speed_preference):
        """
        get the weighted desired distance preference for the given speed preference
        :param speed_preference: 'cautious', 'average', 'speed'
        :return: behind_gap_preference, front_gap_preference, inbetween_gap_preference
        """
        # one-sided behind distance preference
        preference_behind = self.model_settings['speed_distance_preferences'][speed_preference]['behind_gap_preference']
        if preference_behind == 'high':
            behind_gap_preference = self.dist_mean_high
        elif preference_behind == 'avg':
            behind_gap_preference = self.dist_mean_avg
        elif preference_behind == 'small':
            behind_gap_preference = self.dist_mean_small
        else:
            raise ValueError('Unknown behind_gap_preference')

        # one-sided front distance preference
        preference_ahead = self.model_settings['speed_distance_preferences'][speed_preference]['front_gap_preference']
        if preference_ahead == 'high':
            front_gap_preference = self.dist_mean_high
        elif preference_ahead == 'avg':
            front_gap_preference = self.dist_mean_avg
        elif preference_ahead == 'small':
            front_gap_preference = self.dist_mean_small
        else:
            raise ValueError('Unknown front_gap_preference')

        # inbetween distance preference
        preference_inbetween = \
            self.model_settings['speed_distance_preferences'][speed_preference]['inbetween_gap_preference']
        if preference_inbetween == 'small_small':
            inbetween_gap_preference = self.dist_mean_small - self.dist_mean_small
        elif preference_inbetween == 'small_avg':
            inbetween_gap_preference = self.dist_mean_small - self.dist_mean_avg
        elif preference_inbetween == 'small_high':
            inbetween_gap_preference = self.dist_mean_small - self.dist_mean_high
        elif preference_inbetween == 'avg_avg':
            inbetween_gap_preference = self.dist_mean_avg - self.dist_mean_avg
        elif preference_inbetween == 'avg_high':
            inbetween_gap_preference = self.dist_mean_avg - self.dist_mean_high
        elif preference_inbetween == 'high_high':
            inbetween_gap_preference = self.dist_mean_high - self.dist_mean_high
        elif preference_inbetween == 'high_small':
            inbetween_gap_preference = self.dist_mean_high - self.dist_mean_small
        elif preference_inbetween == 'high_avg':
            inbetween_gap_preference = self.dist_mean_high - self.dist_mean_avg
        elif preference_inbetween == 'avg_small':
            inbetween_gap_preference = self.dist_mean_avg - self.dist_mean_small
        else:
            raise ValueError('Unknown inbetween_gap_preference')

        return behind_gap_preference, front_gap_preference, inbetween_gap_preference

    def get_speed_preference(self, behavior, current_curvature):
        """
        get the weighted desired speed preference for the given speed preference behavior and curvature of the tile
        :param behavior: cautious, average, speed
        :param current_curvature: curvature of the tile
        :return: desired mean speed according to curvature
        """
        if behavior == 'cautious':
            for speed, curvature_range in self.curve_preference_cautious.items():
                if curvature_range[0] <= current_curvature <= curvature_range[1]:
                    current_speed_preference = speed
                    break
        elif behavior == 'average':
            for speed, curvature_range in self.curve_preference_average.items():
                if curvature_range[0] <= current_curvature <= curvature_range[1]:
                    current_speed_preference = speed
                    break
        elif behavior == 'speed':
            for speed, curvature_range in self.curve_preference_speed.items():
                if curvature_range[0] <= current_curvature <= curvature_range[1]:
                    current_speed_preference = speed
                    break
        else:
            raise ValueError('Unknown behavior')
        return current_speed_preference

    def get_speed_limit_for_curvature(self, curvature):
        """
        get the speed limit for the given curvature
        :param curvature: curvature of the tile
        :return: speed limit
        """
        for speed, curvature_range in self.speedlimit_to_curvature.items():
            if curvature_range[0] <= curvature <= curvature_range[1]:
                speed_limit = speed
                break
        return speed_limit

    def get_distance_weight(self, behavior):
        """
        gets the amplitude of the distance as weighting for linear combination of distance and speed
        :param behavior: cautious, average, speed
        :return: distance amplitude for weighting
        """
        # one-sided behind distance weights
        preference_behind = self.model_settings['speed_distance_preferences'][behavior]['behind_gap_preference']
        if preference_behind == 'high':
            behind_gap_ampl = self.dist_ampl_high
        elif preference_behind == 'avg':
            behind_gap_ampl = self.dist_ampl_avg
        elif preference_behind == 'small':
            behind_gap_ampl = self.dist_ampl_small
        else:
            raise ValueError('Unknown behind_gap_ampl')

        # one-sided front distance weights
        preference_ahead = self.model_settings['speed_distance_preferences'][behavior]['front_gap_preference']
        if preference_ahead == 'high':
            front_gap_ampl = self.dist_ampl_high
        elif preference_ahead == 'avg':
            front_gap_ampl = self.dist_ampl_avg
        elif preference_ahead == 'small':
            front_gap_ampl = self.dist_ampl_small
        else:
            raise ValueError('Unknown front_gap_ampl')

        return behind_gap_ampl, front_gap_ampl

    def get_speed_weight(self, behavior):
        """
        gets the amplitude of the curve-speed as weighting for linear combination of distance and speed
        :param behavior:
        :return:
        """
        if behavior == 'cautious':
            return self.curve_ampl_cautious
        if behavior == 'average':
            return self.curve_ampl_average
        if behavior == 'speed':
            return self.curve_ampl_speed
        else:
            raise ValueError('Unknown behavior')

    def get_curve_fun_weight(self, current_curvature):
        """
        get the fun out of the curvature
        :param current_curvature: the curvature the motorcyclist is currently on
        :return: how much the fun is weighted depending on curvature. Used for linear combination of speed and distance
        """
        for fun_weight, curvature_range in self.curve_fun_preference.items():
            if curvature_range[0] <= current_curvature <= curvature_range[1]:
                return fun_weight


if __name__ == '__main__':
    config = ConfigPreference('default')
    print(vars(config))
