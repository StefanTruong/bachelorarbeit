from vehicles import *
from tile import *
import numpy as np


class TrafficSimulation:

    def __init__(self, length=10, density=0.3, prob_slowdown=0.1, num_lanes=2, prob_changelane=0.7, car_share=0.9, number_platoons=1, platoon_size=1):
        """
        initializing model parameters
        :param length: length of the trip in tiles. Size of the array. Begins with index 0
        :param density: length*density == #total number of vehicles
        :param prob_slowdown:
        :param num_lanes: begins with index 1 for left lane. Curently works only exactly for 2 lanes!
        :param prob_changelane:
        :param car_share: [0,1]
        :param number_platoons: has to be lower than total number of total vehicles
        :param platoon_size:
        """

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
        self.number_cars = int(round(self.number_other_vehicles*car_share))
        self.number_bikes = self.number_other_vehicles - self.number_cars


    def generic_tile_setter(self):
        """
        generates a street with Tiles for each lane and randomly sets cars and bikes on the street
        :return: array of tiles = [(left_Tile, right_Tile)] with tuple representing a street sector
        """

        # generates my empty street
        tiles = []
        for index in range(0, self.length):
            street_sector = []

            for lane in range(1, self.num_lanes+1):
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
                tile = tiles[pos][1]
                bike = Bike(speed=3, tile=tile)
                tiles[pos][1].vehicle = car

        # motorcyclists are positioned on the left side at the beginning of the trip, with speed=0
        tile_index = 0
        for platoon in range(0, self.number_platoons):
            tile = tiles[tile_index][0]

            for biker in range(0, self.number_total_motorcycles):
                motorcyclist = Motorcycle(speed=0, tile=tile)
                tiles[tile_index][0].vehicle = motorcyclist
                tile_index += 1

        return tiles, random_pos_of_cars_and_bikes


    def initialize(self):
        tiles, random_pos_of_cars_and_bikes = self.generic_tile_setter()





simulation = TrafficSimulation()
simulation.initialize()
