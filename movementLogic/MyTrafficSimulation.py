import math
from vehicles.Motorcycle import Motorcycle
from vehicles.Vehicles import *
from StreetAttributes.tile import *
import numpy as np
from plotAndVisualize.visualizer import VisualizeStreet


class TrafficSimulation:

    def __init__(self, length, total_amount_steps, density, num_lanes, prob_slowdown, prob_changelane, car_share,
                 number_platoons, platoon_size, car_max_velocity, bike_max_velocity, motorcycle_max_velocity,
                 speed_preferences=None, distance_preferences=None, speed_distance_preferences=None,
                 biker_composition_modus=None, adjust_speed_preference=False):
        """
        initializing model parameters
        :param length: length of the trip in tiles. Size of the array. Begins with index 0
        :param density: length*density == #total number of vehicles. Value between [0,2]
        :param prob_slowdown:
        :param num_lanes: begins with index 0 for left lane. Currently, works only exactly for 2 lanes!
        :param prob_changelane: changing_lane L->R for overtaking
        :param car_share: [0,1]
        :param number_platoons: has to be lower than total number of total vehicles
        :param platoon_size: has to be greater than 1
        :param speed_preferences: list of preferences for speed
        :param total_amount_steps: determines how many steps the simulation stops
        """
        self.vehicle_list = None  # will be initialized in method generic_tiles_setter
        self.tiles = None  # will be initialized in method generic_tiles_setter [(left_Tile, right_Tile), ...]
        self.length = length
        self.total_amount_steps = total_amount_steps
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
        if self.number_other_vehicles < 0:
            raise Exception("Too many Motorcycles for given vehicle density. Choose less Motorcyclist")

        self.number_cars = int(round(self.number_other_vehicles * car_share))
        self.number_bikes = self.number_other_vehicles - self.number_cars

        self.car_max_velocity = car_max_velocity
        self.bike_max_velocity = bike_max_velocity
        self.motorcycle_max_velocity = motorcycle_max_velocity

        self.speed_preferences = speed_preferences
        self.distance_preferences = distance_preferences
        self.speed_distance_preferences = speed_distance_preferences
        self.biker_composition_modus = biker_composition_modus
        self.adjust_speed_preference = adjust_speed_preference

        self.platoon_composition = None  # equal: ['cautious', 'cautious', 'average', 'speed']
        self.distribute_biker_speed_preference()

        self.preference_object = None
        self.config_object = None

    def distribute_biker_speed_preference(self):
        """
        set up how the speed preferences in a platoon is distributed in a list
        e.g. for equal distribution ['cautious', 'cautious', 'average', 'speed']
        :return:
        """
        platoon_composition = None
        if self.biker_composition_modus == 'equal':
            platoon_composition_split = np.array_split([None] * self.platoon_size, len(self.speed_preferences))
            platoon_composition = list()

            for split_index, preference in enumerate(self.speed_preferences):
                speed_preference = preference
                length = len(platoon_composition_split[split_index])
                part = [speed_preference] * length
                platoon_composition += part

        elif self.biker_composition_modus == 'cautious_only':
            if self.speed_preferences[0] == 'cautious':
                platoon_composition = ['cautious'] * self.platoon_size
            else:
                raise ValueError('Unknown speed preference')

        elif self.biker_composition_modus == 'average_only':
            if self.speed_preferences[1] == 'average':
                platoon_composition = ['average'] * self.platoon_size

        elif self.biker_composition_modus == 'speed_only':
            if self.speed_preferences[2] == 'speed':
                platoon_composition = ['speed'] * self.platoon_size
        else:
            raise ValueError("No other biker_composition_modus implemented yet")

        self.platoon_composition = platoon_composition

    def generate_empty_street(self):
        """
        generates an empty street
        array of tiles = [(left_Tile, right_Tile), ...] with tuple representing a street sector
        :return: returns empty street
        """
        tiles = []
        for index in range(0, self.length):
            street_sector = []

            for lane in range(0, self.num_lanes + 1):
                tile = Tile(index=index, lane=lane)
                street_sector.append(tile)

            street_sector = tuple(street_sector)
            tiles.append(street_sector)

        return tiles

    @staticmethod
    def generate_random_placing_number(length, number_vehicles):
        """
        generates random number
        :return: returns a ndarray index number where cars and bikes should be placed e.g. [43,81,83,82]
        """
        return np.random.choice(length, size=number_vehicles, replace=False)

    def placing_cars_bikes(self, tiles, vehicle_list, free_elements, positions, num_cars, num_bikes):
        """
        places cars and bikes randomly on the street required it is free. Starting with speed=0
        populates a vehicle_list where all vehicles are listed
        :param free_elements: list of [(idx, lane), ...] of free tiles
        :param num_bikes: number of bikes which should be placed
        :param num_cars: number of cars which should be placed
        :param vehicle_list: the list of all vehicles Cars Bikes and Motorcyclist
        :param tiles: the tiles on which the vehicles will be placed on
        :param positions: list of numbers where cars and bikes should be positioned on the lane
        """

        for index, pos in enumerate(positions):
            idx = free_elements[pos][0]
            lane = free_elements[pos][1]
            tile = tiles[idx][lane]

            if index < num_cars:
                car = Car(speed=0, tile=tile, max_velocity=self.car_max_velocity)
                if tiles[idx][lane].get_vehicle() is None:
                    tiles[idx][lane].set_vehicle(car)
                    vehicle_list.append(car)
                else:
                    raise Exception('Problem in car placing. Place is not available')

            else:
                bike = Bike(speed=0, tile=tile, max_velocity=self.bike_max_velocity)
                if tiles[idx][lane].get_vehicle() is None:
                    tiles[idx][lane].set_vehicle(bike)
                    vehicle_list.append(bike)
                else:
                    raise Exception('Problem in Bike placing. Place is not available')

    def placing_motorcyclist(self, tiles, vehicle_list):
        """
        motorcyclists are placed on the left lane beginning with index = 0 with speed=0
        if there are more platoons, then they will be offset equally
        :return:
        """
        # calculate offset between different platoons
        free_space = self.length - self.number_total_motorcycles
        if free_space < 0:
            raise Exception("There are too many motorcycles. Choose a lower number of platoons or shrink size")
        offset = int(math.floor(free_space / self.number_platoons))

        tile_index = 0
        for platoon in range(0, self.number_platoons):
            last_motorcyclist = None

            for biker_number in range(0, self.platoon_size):
                tile = tiles[tile_index][0]

                if self.platoon_composition is not None:
                    preferred_speed = self.platoon_composition[biker_number]
                else:
                    preferred_speed = None

                motorcyclist = Motorcycle(speed=0, tile=tile, group=platoon,
                                          preferred_speed=preferred_speed,
                                          max_velocity=self.motorcycle_max_velocity)

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

            # offset between each platoon
            tile_index += offset

    def look_free_tiles(self, tiles):
        """
        creates a list of (idx, lane) of free tiles on the street s.t. we can place the cars and bikes randomly
        :param tiles: The street
        :return: returns a list of [(idx, lane), ...] of free tiles
        """
        free_elements = []
        for sector in tiles:
            for lane in range(0, self.num_lanes + 1):
                if sector[lane].get_vehicle() is None:
                    free = (sector[lane].get_index(), lane)
                    free_elements.append(free)

        return free_elements

    def generic_tile_setter(self):
        """
        generates a street with Tiles for each lane and randomly sets cars and bikes on the street
        """
        vehicle_list = []
        tiles = self.generate_empty_street()

        # motorcyclists are positioned on the left side at the beginning of the trip, with speed=0.
        self.placing_motorcyclist(tiles, vehicle_list)

        # get free space of the street tiles to randomly place the cars and Bikes
        free_elements = self.look_free_tiles(tiles)

        # choose from the free space for placing cars and bikes
        random_pos_of_others = self.generate_random_placing_number(len(free_elements), self.number_other_vehicles)

        # place cars and bikes on street
        self.placing_cars_bikes(tiles, vehicle_list, free_elements, random_pos_of_others, self.number_cars,
                                self.number_bikes)

        self.tiles = tiles
        self.vehicle_list = vehicle_list[::-1]
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

        :param update_speed_modus: when Motorcyclist should update its speed according to its speed-gap preference
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
            if self.adjust_speed_preference and type(vehicle) is Motorcycle:
                vehicle.update_speed_preference()
            else:
                vehicle.update_speed()

            # move all vehicles to its updated speed in the tiles
            self.move_vehicle(vehicle)

            # after moving prepare for switching lane
            self.update_lane_position(vehicle)

            # which visualization should be used
            if vis_modus == 'step':
                vis.traffic_vis_tiles_step_by_step(vehicle, display_curve=True)
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

    def get_number_total_vehicles(self):
        return self.number_total_vehicles

    @staticmethod
    def set_uniqueid(vehicle_list: list):
        identifier = 0
        for vehicle in vehicle_list:
            vehicle.set_id(identifier)
            identifier += 1

    def get_preference_object(self):
        return self.preference_object

    def get_config_object(self):
        return self.config_object

    def set_preference_object(self, preference_object):
        self.preference_object = preference_object

    def set_config_object(self, cfg):
        self.config_object = cfg
