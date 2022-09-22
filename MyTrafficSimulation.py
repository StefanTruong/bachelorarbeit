from vehicles import *
from tile import *
import numpy as np
import sys


def traffic_visualization_tiles(simulation):
    """
    visualizes the street on console.
    :param simulation:
    :return:
    """
    tiles = simulation.tiles
    lanes = simulation.num_lanes
    length = simulation.length

    # Make sure we have space to draw the lanes
    # sys.stdout.write("\n" * lanes)

    for lane in range(0, lanes + 1):
        for tile in tiles:
            visual = tile[lane].get_icon()
            sys.stdout.write(visual)
        sys.stdout.write('\n')


class TrafficSimulation:

    def __init__(self, length, density, prob_slowdown, num_lanes, prob_changelane, car_share,
                 number_platoons, platoon_size, speed_preferences):
        """
        initializing model parameters
        :param length: length of the trip in tiles. Size of the array. Begins with index 0
        :param density: length*density == #total number of vehicles
        :param prob_slowdown:
        :param num_lanes: begins with index 0 for left lane. Curently works only exactly for 2 lanes!
        :param prob_changelane:
        :param car_share: [0,1]
        :param number_platoons: has to be lower than total number of total vehicles
        :param platoon_size: has to be greater than 1
        :param speed_preferences: dict : dict : dict
        """

        self.tiles = None  # will be initialized in method generic_tiles_setter [(left_Tile, right_Tile), ...]
        self.length = length
        self.density = density
        self.prob_slowdown = prob_slowdown
        self.num_lanes = num_lanes
        self.prob_changelane = prob_changelane
        self.car_share = car_share
        self.number_total_vehicles = int(round(length * density))
        self.number_platoons = number_platoons
        self.platoon_size = platoon_size
        self.number_total_motorcycles = number_platoons * platoon_size
        self.number_other_vehicles = self.number_total_vehicles - self.number_total_motorcycles
        self.number_cars = int(round(self.number_other_vehicles * car_share))
        self.number_bikes = self.number_other_vehicles - self.number_cars
        self.speed_preferences = speed_preferences

        biker_composition_modus = 1  # {speedy, average, cautious} ToDo Inputparameter
        keys = list(speed_preferences.keys())
        platoon_composition_split = np.array_split([None] * self.platoon_size, len(keys))
        platoon_composition = list()

        if biker_composition_modus == 1:
            for split_index, key in enumerate(keys):
                speed_preference = {key: speed_preferences[key]}
                length = len(platoon_composition_split[split_index])
                part = [speed_preference] * length
                platoon_composition += part

        self.platoon_composition = platoon_composition
        self.step = 0
        self.flow = 0

    def generic_tile_setter(self):
        """
        generates a street with Tiles for each lane and randomly sets cars and bikes on the street
        :return: array of tiles = [(left_Tile, right_Tile)] with tuple representing a street sector
        """

        # generates my empty street
        tiles = []
        for index in range(0, self.length):
            street_sector = []

            for lane in range(0, self.num_lanes + 1):
                tile = Tile(index=index, lane=lane)
                street_sector.append(tile)

            street_sector = tuple(street_sector)
            tiles.append(street_sector)

        # creates a ndarray containing index number where cars and bikes should be placed
        random_pos_of_cars_and_bikes = np.random.choice(self.length, size=self.number_other_vehicles, replace=False)

        # cars and bikes are always positioned on the left side lane. Starting with speed=3
        for index, pos in enumerate(random_pos_of_cars_and_bikes):
            tile = tiles[pos][1]

            if index < self.number_cars:
                car = Car(speed=3, tile=tile)
                tiles[pos][1].vehicle = car

            else:
                bike = Bike(speed=3, tile=tile)
                tiles[pos][1].vehicle = bike

        # motorcyclists are positioned on the left side at the beginning of the trip, with speed=0
        tile_index = 0
        for platoon in range(0, self.number_platoons):
            tile = tiles[tile_index][0]

            for biker_number in range(0, self.platoon_size):
                motorcyclist = Motorcycle(speed=0, tile=tile, group=platoon,
                                          prefered_speed=self.platoon_composition[biker_number])
                tiles[tile_index][0].vehicle = motorcyclist
                tile_index += 1

        self.tiles = tiles

    def initialize(self):
        self.generic_tile_setter()


def change_lane(trafficsimulation):
    pass


# Has to be set in class Trafficsimulation again
model_settings = {
    'length': 12000,
    'density': 0.2,
    'prob_slowdown': 0.1,
    'num_lanes': 1,
    'prob_changelane': 0.7,
    'car_share': 0.9,
    'number_platoons': 2,
    'platoon_size': 4,
    'speed_preferences': {
        'cautious': None,
        'average': None,
        'speedy': None,
    }
}

sim = TrafficSimulation(**model_settings)
sim.initialize()
traffic_visualization_tiles(sim)
