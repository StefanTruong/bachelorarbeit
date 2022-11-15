from tile import *
from vehicles import *
import numpy as np
import time, sys, random


class VisualizeStreet:

    def __init__(self, simulation):
        """
        :param simulation: Object from MyTrafficSimulation to get a reference
        """
        # time_space_data is used for storing data across each visualization call
        # {0: [ [], [], ..., [] ],
        #  1: [ [], [], ..., [] ]}
        self.time_space_data = dict()
        self.simulation = simulation

    def traffic_vis_tiles(self):
        """
        simply plots the street with the vehicles on it
        :return:
        """
        for lane in range(0, self.simulation.num_lanes + 1):
            visual = ''
            for tile in self.simulation.tiles:
                visual += tile[lane].get_icon()
            sys.stdout.write(visual)
            sys.stdout.write('\n')

    def traffic_vis_tiles_step_by_step(self, vehicle: Vehicle):
        """
        visualizes the street on console step by step for each vehicle
        X is the marker in which position the vehicle has moved
        :param vehicle: the vehicle which is moved. Position of it is needed for marker
        :return:
        """
        marker = ''
        for i in range(vehicle.get_tile().get_index()):
            marker += '     '
        marker += '  X  '

        print(marker)
        for lane in range(0, self.simulation.num_lanes + 1):
            for tile in self.simulation.tiles:
                visual = tile[lane].get_icon()
                sys.stdout.write(visual)
            sys.stdout.write('\n')

        sys.stdout.write('\n')

    def traffic_vis_tiles_fix_lines(self):
        """
        visualizes the street in fixed two lines
        :return:
        """
        # print visual line by line
        for lane in range(0, self.simulation.num_lanes + 1):
            visual_line_str = ""
            for tile in self.simulation.tiles:
                visual_line_str = visual_line_str + tile[lane].get_icon()

            print(visual_line_str)

        # move left
        sys.stdout.write(u"\u001b[10000D")
        # Move up
        sys.stdout.write(u"\u001b[" + "2" + "A")

    def traffic_vis_tiles_fix_lines_focused(self, focus_vehicle: Vehicle):
        """
        visualizes the street in fixed two lines before and after a focused vehicle
        :param focus_vehicle: the vehicle the visualization should focus on
        :return:
        """
        view_distance = 22  # how far should be displayed

        # calculates the right index to display
        behind = (focus_vehicle.get_tile().get_index() - view_distance) % self.simulation.get_length()
        ahead = (focus_vehicle.get_tile().get_index() + view_distance) % self.simulation.get_length()
        length = self.simulation.get_length()

        # print visual line by line
        for lane in range(0, self.simulation.num_lanes + 1):
            visual_line_str = ""
            for incr in range(0, view_distance * 2 + 1):
                visual_line_str += self.simulation.get_tiles()[(behind + incr) % length][lane].get_icon()
            print(visual_line_str)

        # move left
        sys.stdout.write(u"\u001b[10000D")
        # Move up
        sys.stdout.write(u"\u001b[" + "2" + "A")

    # ToDo Plot to a 2D Pixel Plot
    def traffic_vis_tiles_granular(self):
        """
        writes one side of the time space diagram and plots it into a 2D Pixel Plot
        :return: 2D Pixel Plot
        """
        # Dict to flexible naming variables according to lane
        # Array represents x-axis of the 2D Plot, subarray y-axis of one side of the lane
        # {0: [],
        #  1: []}
        x_values_all_lanes_all_steps = dict()

        for lane in range(0, self.simulation.num_lanes + 1):
            x_values_step = []

            for tile in self.simulation.tiles:
                x_values_step.append(tile[lane].get_icon_granular())

            x_values_all_lanes_all_steps[lane] = x_values_step

            # the time_space_data is a dict with a list as value. But Interpreter does not know that at first
            if lane not in self.time_space_data:
                self.time_space_data[lane] = list()
                self.time_space_data[lane].append(x_values_all_lanes_all_steps[lane])
            else:
                self.time_space_data[lane].append(x_values_all_lanes_all_steps[lane])

    def get_time_space_data(self, lane):
        """
        returns the time space data for plotting
        :param lane: lane side which should be returned
        :return: time space data in a list of lists
        """
        return self.time_space_data[lane]
