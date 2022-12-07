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
        'motorcycle_max_velocity': 7, }
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
        'motorcycle_max_velocity': 7, }
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
        'motorcycle_max_velocity': 7, }
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
        'motorcycle_max_velocity': 7, }
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
        'motorcycle_max_velocity': 7, }
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
        'motorcycle_max_velocity': 7, }
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
        'motorcycle_max_velocity': 7, }
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
        'motorcycle_max_velocity': 7, }
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
            modi equal: equal distribution of speed_preferences in the platoon
                        Beginning with cautious first, then average and then speed
            """
            self.model_settings = {
                'length': 1000,
                'total_amount_steps': 100,
                'density': 0.1,
                'num_lanes': 1,  # [0,1] do not change
                'prob_slowdown': 0.1,
                'prob_changelane': 1,
                'car_share': 1,
                'number_platoons': 1,
                'platoon_size': 4,
                'car_max_velocity': 10,
                'bike_max_velocity': 2,
                'motorcycle_max_velocity': 7,
                'speed_preferences': ['cautious', 'average', 'speed'],
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

        # # Preference Settings
        # distance preference single sided
        self.dist_mean_small = 6
        self.dist_sd_small = 1
        self.dist_ampl_small = 1
        self.dist_mean_avg = 8
        self.dist_sd_avg = 1
        self.dist_ampl_avg = 1
        self.dist_mean_high = 10
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

        # From tileAttrSetting.py curve-speed-limit
        self.speedlimit_to_curvature = {
            10: (0, 500),  # 10tiles ~ 40 m/s ~ 144 km/h
            9: (500, 800),  # 9 tiles ~ 36 m/s ~ 129 km/h
            8: (800, 1000),  # 8 tiles ~ 32 m/s ~ 115 km/h
            7: (1000, 1200),  # 7 tiles ~ 28 m/s ~ 101 km/h
            6: (1200, 1400),  # 6 tiles ~ 24 m/s ~ 86 km/h
            5: (1400, 1600),  # 5 tiles ~ 20 m/s ~ 72 km/h
            4: (1600, 1800),  # 4 tiles ~ 16 m/s ~ 57 km/h
            3: (1800, 2000),  # 3 tiles ~ 12 m/s ~ 43 km/h
            2: (2000, 3000),  # 2 tiles ~ 8 m/s ~ 29 km/h
            1: (3000, 10000),  # 1 tile ~ 4 m/s ~ 14 km/h
        }
        # The speed type wants to ride maximum speed
        self.curve_preference_speed = self.speedlimit_to_curvature

        # The average type wants to ride one speed less
        self.curve_preference_average = {
            9: (0, 500),
            8: (500, 800),
            7: (800, 1000),
            6: (1000, 1200),
            5: (1200, 1400),
            4: (1400, 1600),
            3: (1600, 1800),
            2: (1800, 3000),
            1: (3000, 10000),
        }

        # The cautious type wants to ride two speed less
        self.curve_preference_cautious = {
            8: (0, 500),
            7: (500, 800),
            6: (800, 1000),
            5: (1000, 1200),
            4: (1200, 1400),
            3: (1400, 1600),
            2: (1600, 3000),
            1: (3000, 10000),
        }


if __name__ == '__main__':
    config = ConfigPreference('default')
    print(vars(config))
