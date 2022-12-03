import numpy as np

# distance preference single sided
dist_mean_small = 6
dist_sd_small = 1
dist_ampl_small = 1
dist_mean_avg = 8
dist_sd_avg = 1
dist_ampl_avg = 1
dist_mean_high = 10
dist_sd_high = 1
dist_ampl_high = 1

# curve speed preference
curve_preference_cautious = None  # ToDo Input parameter
curve_preference_average = None  # ToDo Input parameter
curve_preference_speed = None  # ToDo Input parameter
curve_sd_cautious = 1
curve_ampl_cautious = 1
curve_sd_average = 1
curve_ampl_average = 1
curve_sd_speed = 1
curve_ampl_speed = 1

# How far the NV should be calculated. Length of data has to match with length for pdf and gradient to match
dist_preference_sight = np.linspace(0, 50, 50)

# From tileAttrSetting.py curve-speed-limit
speedlimit_to_curvature = {
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
curve_preference_speed = speedlimit_to_curvature

# The average type wants to ride one speed less
curve_preference_average = {
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
curve_preference_cautious = {
    8: (0, 500),
    7: (500, 800),
    6: (800, 1000),
    5: (1000, 1200),
    4: (1200, 1400),
    3: (1400, 1600),
    2: (1600, 3000),
    1: (3000, 10000),
}
