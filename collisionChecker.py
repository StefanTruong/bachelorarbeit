from tile import *
import sys
import copy
import tile


class CollisionChecker:
    number_of_collisions = 0
    number_of_missing_pos = 0
    simulation = None
    all_vehicle_present = True

    def __init__(self, simulation):
        self.simulation = simulation
        self.initial_vehicle_list = copy.deepcopy(simulation.vehicle_list)
        self.initial_vehicle_id_list = []

        for vehicle in self.initial_vehicle_list:
            self.initial_vehicle_id_list.append(vehicle.get_id())

    def check_for_inconsistencies(self):
        """
        checks for inconsistencies like vanishing cars and collisions
        :return:
        """
        self.check_for_vehicle_collision()
        self.check_for_missing_index()
        # ToDo this should be called separately after initial debugging is done due to performance reasons!
        # self.check_all_vehicle_present()

    def check_for_vehicle_collision(self):
        """
        checks if a vehicle shares a tile with another vehicle aka if a collisions happened
        :return:
        """
        vehicle_idx_lane_list = []  #[(idx, lane)]

        for vehicle in self.simulation.vehicle_list:
            idx = vehicle.get_tile().get_index()
            lane = vehicle.get_tile().get_lane()
            idx_lane = [idx, lane]
            vehicle_idx_lane_list.append(tuple(idx_lane))

        my_set = set(vehicle_idx_lane_list)

        if len(vehicle_idx_lane_list) != len(my_set):
            sys.stdout.write(f'Collision for vehicle in (pos, lane): '
                             f'{vehicle.get_tile().get_index(), vehicle.get_tile().get_lane()}')
            sys.stdout.write('\n')
            self.number_of_collisions += 1

    def check_for_missing_index(self):
        """
        checks if a vehicle has no tile reference
        :return:
        """
        for vehicle in self.simulation.vehicle_list:
            if vehicle.get_tile().get_index() is None:
                sys.stdout.write(f'vehicle has no tile: {vehicle.get_icon()}')
                sys.stdout.write('\n')
                self.number_of_missing_pos += 1

    def check_all_vehicle_present(self):
        """
        checks if a vehicle vanishes during a step or a new vehicle suddenly appears after initial setting
        :return:
        """
        current_vehicle_ids_on_street = []

        # get all vehicles on the street
        for section in self.simulation.tiles:
            for tile in section:
                if tile.get_vehicle() is not None:
                    current_vehicle_ids_on_street.append(tile.get_vehicle().get_id())

        all_present = all(vehicle_id in self.initial_vehicle_id_list for vehicle_id in current_vehicle_ids_on_street)

        if not all_present:
            self.all_vehicle_present = False
