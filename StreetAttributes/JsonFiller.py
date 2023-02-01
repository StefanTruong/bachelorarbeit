import pandas as pd
import json
from configuration.config import ConfigPreference

# fills the street data in json format ########################################

# load csv file as df and configuration file
street_data = pd.read_csv('./Streets/teststreet.csv', sep=',', header=0)

# print(street_data.columns.tolist())
cfg = ConfigPreference()

# create empty dict
street_dict = dict()
current_filled_index = 0    # the index of street_dict which is currently filled

for index, row in street_data.iterrows():
    # get data from csv file if available
    # Hint: values will be set section wise and not tile wise. Meaning the whole section will have the same values

    # km cannot be 0 or empty
    if row['km'] == 0:
        street_length = 1
    else:
        street_length = row['km']

    if row['curvature'] != -1:
        curvature = row['curvature'] / street_length
    else:
        curvature = 0

    #  speedlimit will be used from config instead of data
    speed_limit = cfg.get_speed_limit_for_curvature(curvature)

    # beauty will not be used for analysis since there are no data available
    if row['beauty'] == -1 or row['beauty'] == '':
        beauty = 0
    else:
        beauty = row['beauty']

    # append the values to the street_dict according to how long the street is. One tile is 3m
    number_entries = int(street_length * 1000 / 3)
    increment = 0
    for i in range(current_filled_index, current_filled_index + number_entries):
        street_dict[i] = [curvature, speed_limit, beauty]
        increment += 1

    current_filled_index += increment

# save the street_dict as json file
with open('./attr_list.json', 'w') as f:
    json.dump(street_dict, f)