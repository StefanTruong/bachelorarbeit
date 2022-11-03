import time

from vehicles import *
from tile import *
import numpy as np
import sys
from visualizer import VisualizeStreet
from collisionChecker import CollisionChecker


class TrafficSimulation:

    def __init__(self, length, density, num_lanes, prob_slowdown, prob_changelane, car_share,
                 number_platoons, platoon_size, speed_preferences, total_amount_steps):
        """
        initializing model parameters
        :param length: length of the trip in tiles. Size of the array. Begins with index 0
        :param density: length*density == #total number of vehicles
        :param prob_slowdown:
        :param num_lanes: begins with index 0 for left lane. Curently works only exactly for 2 lanes!
        :param prob_changelane: changing_lane L->R for overtaking
        :param car_share: [0,1]
        :param number_platoons: has to be lower than total number of total vehicles
        :param platoon_size: has to be greater than 1
        :param speed_preferences: dict : dict : dict
        :param total_amount_steps: determines how many steps the simulation stops
        """

        self.vehicle_list = None  # will be initialized in method generic_tiles_setter
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

        biker_composition_modus = 1  # {cautious, average, speedy} ToDo as Input parameter
        keys = list(speed_preferences.keys())
        platoon_composition_split = np.array_split([None] * self.platoon_size, len(keys))
        # e.g. 5Motos [[{'cautious':None}, {'cautious':None}], [{'average':None}, {'average':None}], [{'speedy':None}]]
        platoon_composition = list()

        if biker_composition_modus == 1:
            for split_index, key in enumerate(keys):
                speed_preference = {key: speed_preferences[key]}
                length = len(platoon_composition_split[split_index])
                part = [speed_preference] * length
                platoon_composition += part

        self.platoon_composition = platoon_composition
        self.total_amount_steps = total_amount_steps

    def generic_tile_setter(self):
        """
        generates a street with Tiles for each lane and randomly sets cars and bikes on the street
        :param: array of tiles = [(left_Tile, right_Tile), ...] with tuple representing a street sector
        """
        vehicle_list = []

        # generates my empty street without curvature
        tiles = []
        for index in range(0, self.length):
            street_sector = []

            for lane in range(0, self.num_lanes + 1):
                tile = Tile(index=index, lane=lane)
                street_sector.append(tile)

            street_sector = tuple(street_sector)
            tiles.append(street_sector)

        # creates a ndarray containing index number where cars and bikes should be placed e.g. [43,81,83,82]
        random_pos_of_cars_and_bikes = np.random.choice(self.length, size=self.number_other_vehicles, replace=False)

        # cars and then bikes are always first positioned on the right side lane. Starting with speed=0
        for index, pos in enumerate(random_pos_of_cars_and_bikes):
            tile = tiles[pos][1]

            if index < self.number_cars:
                car = Car(speed=0, tile=tile)
                tiles[pos][1].set_vehicle(car)
                vehicle_list.append(car)

            else:
                bike = Bike(speed=0, tile=tile)
                tiles[pos][1].set_vehicle(bike)
                vehicle_list.append(bike)

        # motorcyclists are positioned on the left side at the beginning of the trip, with speed=0.
        tile_index = 0
        for platoon in range(0, self.number_platoons):
            last_motorcyclist = None

            for biker_number in range(0, self.platoon_size):
                tile = tiles[tile_index][0]
                motorcyclist = Motorcycle(speed=0, tile=tile, group=platoon,
                                          prefered_speed=self.platoon_composition[biker_number])

                # chain motorcyclist in a platoon together
                if last_motorcyclist is not None:
                    motorcyclist.set_behind_partner(last_motorcyclist)
                    last_motorcyclist.set_ahead_partner(motorcyclist)
                    last_motorcyclist = motorcyclist
                else:
                    last_motorcyclist = motorcyclist

                tiles[tile_index][0].set_vehicle(motorcyclist)
                vehicle_list.append(motorcyclist)
                tile_index += 1
            tile_index += 10

        self.tiles = tiles
        self.vehicle_list = vehicle_list
        self.set_uniqueid(vehicle_list)

    def initialize(self):
        """
        set up the vehicles and the street. Each vehicle gets reference to the simulation
        :return:
        """
        self.generic_tile_setter()
        for vehicle in self.vehicle_list:
            vehicle.set_MyTrafficSimulation(self)

    def update_lane_position(self, vehicle: Vehicle):
        """
        asks a vehicle if it would like to switch lane and updates the tiles
        :return:
        """
        if vehicle.check_switch_position():
            current_tile = vehicle.get_tile()
            current_lane = current_tile.get_lane()
            current_idx = current_tile.get_index()

            if current_lane == 0:
                other_lane = 1
            elif current_lane == 1:
                other_lane = -1

            # frees old tile from vehicle
            self.tiles[current_idx][current_lane].set_vehicle(None)
            # sets vehicle on the other lane
            self.tiles[current_idx][current_lane + other_lane].set_vehicle(vehicle)
            # updates current tile in the vehicle obj
            vehicle.set_tile(self.tiles[current_idx][current_lane + other_lane])

    def move_vehicle(self, vehicle: Vehicle):
        """
        moves the vehicle according to its speed and updates the tiles on the same lane
        :param vehicle:
        :return:
        """
        current_speed = vehicle.get_speed()
        current_tile = vehicle.get_tile()
        current_lane = current_tile.get_lane()
        current_idx = current_tile.get_index()

        # free old tile from vehicle
        self.tiles[current_idx][current_lane].set_vehicle(None)
        # moves vehicle forward according to its speed
        self.tiles[(current_idx + current_speed) % self.length][current_lane].set_vehicle(vehicle)
        # updates current tile in the vehicle obj
        vehicle.set_tile(self.tiles[(current_idx + current_speed) % self.length][current_lane])

    def moving_each_vehicle(self, vis: VisualizeStreet):
        """
        starts the simulation by moving the vehicles on the lane. Does not update the speed nor change the lane itself
        :return:
        """
        for vehicle in self.vehicle_list:
            # first update speed of all vehicles according to its surroundings
            vehicle.update_speed()

            # move all vehicles to its updated speed in the tiles
            self.move_vehicle(vehicle)

            # after moving prepare for switching lane
            self.update_lane_position(vehicle)
            vis.traffic_vis_tiles_step_by_step(vehicle)

    def moving_fix_line(self, vis: VisualizeStreet):
        """
        starts the simulation by moving the vehicles on the lane on fixed lines
        :return:
        """
        for vehicle in self.vehicle_list:
            # first update speed of all vehicles according to its surroundings
            vehicle.update_speed()

            # move all vehicles to its updated speed in the tiles
            self.move_vehicle(vehicle)

            # after moving prepare for switching lane
            self.update_lane_position(vehicle)
            vis.traffic_vis_tiles_fix_lines()

    def moving_focused(self, vis: VisualizeStreet, focus_vehicle: Vehicle):
        """
        starts the simulation by moving the vehicles on the lane. Does not update the speed nor change the lane itself
        :return:
        """
        for vehicle in self.vehicle_list:
            # first update speed of all vehicles according to its surroundings
            vehicle.update_speed()

            # move all vehicles to its updated speed in the tiles
            self.move_vehicle(vehicle)

            # after moving prepare for switching lane
            self.update_lane_position(vehicle)
            vis.traffic_vis_tiles_fix_lines_focused(focus_vehicle)

    def moving(self, vis: VisualizeStreet = None, vis_modus=None, focused_vehicle=None):
        """

        :param vis: vis object
        :param focused_vehicle: the vehicle it should be focused on
        :param vis_modus: which vis function should be called
        fix:        uses vis.traffic_vis_tiles_fix_lines()
        step:       uses vis.traffic_vis_tiles_step_by_step()
        focused:    uses vis.traffic_vis_tiles_fix_lines_focused()
        :return:
        """
        for vehicle in self.vehicle_list:
            # first update speed of all vehicles according to its surroundings
            vehicle.update_speed()

            # move all vehicles to its updated speed in the tiles
            self.move_vehicle(vehicle)

            # after moving prepare for switching lane
            self.update_lane_position(vehicle)

            # which visualization should be used
            if vis_modus == 'step':
                vis.traffic_vis_tiles_step_by_step(vehicle)
            elif vis_modus == 'fix':
                vis.traffic_vis_tiles_fix_lines()
            elif vis_modus == 'focused':
                vis.traffic_vis_tiles_fix_lines_focused(focused_vehicle)
            else:
                pass

    def get_tiles(self):
        return self.tiles

    def get_vehicle_list(self):
        return self.vehicle_list

    def get_length(self):
        return self.length

    def get_density(self):
        return self.density

    def get_lanes(self):
        return self.num_lanes

    @staticmethod
    def set_uniqueid(vehicle_list: list):
        identifier = 0
        for vehicle in vehicle_list:
            vehicle.set_id(identifier)
            identifier += 1
