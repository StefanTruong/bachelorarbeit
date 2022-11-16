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

    def traffic_vis_tiles(self, display_curve=False):
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

        if display_curve:
            curve_visual = ''
            for tile in self.simulation.tiles:
                curve_visual += str(tile[0].get_icon_curve())
            sys.stdout.write(curve_visual)
            sys.stdout.write('\n')

    def traffic_vis_tiles_step_by_step(self, vehicle: Vehicle, display_curve=False):
        """
        visualizes the street on console step by step for each vehicle
        X is the marker in which position the vehicle has moved
        :param display_curve: should the curve of the street be displayed
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

        if display_curve:
            curve_visual = ''
            for tile in self.simulation.tiles:
                curve_visual += str(tile[0].get_icon_curve())
            sys.stdout.write(curve_visual)
            sys.stdout.write('\n')

        sys.stdout.write('\n')

    def traffic_vis_tiles_fix_lines(self, display_curve=False):
        """
        visualizes the street in fixed two lines
        :return:
        """
        if display_curve:
            shift_carret = "3"
        else:
            shift_carret = "2"

        # print visual line by line
        for lane in range(0, self.simulation.num_lanes + 1):
            visual_line_str = ""
            for tile in self.simulation.tiles:
                visual_line_str = visual_line_str + tile[lane].get_icon()

            print(visual_line_str)

        if display_curve:
            visual_curve_str = ""
            for tile in self.simulation.tiles:
                visual_curve_str = visual_curve_str + tile[0].get_icon_curve()
            print(visual_curve_str)

        # move left
        sys.stdout.write(u"\u001b[10000D")
        # Move up
        sys.stdout.write(u"\u001b[" + shift_carret + "A")

    def traffic_vis_tiles_fix_lines_focused(self, focus_vehicle: Vehicle, display_curve=False):
        """
        visualizes the street in fixed two lines before and after a focused vehicle
        :param display_curve: should the curve of the street be displayed
        :param focus_vehicle: the vehicle the visualization should focus on
        :return:
        """
        view_distance = 10  # how far should be displayed before and after the focused vehicle

        if display_curve:
            shift_carret = "3"
        else:
            shift_carret = "2"

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

        if display_curve:
            visual_curve_str = ""
            for incr in range(0, view_distance * 2 + 1):
                visual_curve_str += self.simulation.get_tiles()[(behind + incr) % length][0].get_icon_curve()
            print(visual_curve_str)


        # move left
        sys.stdout.write(u"\u001b[10000D")
        # Move up
        sys.stdout.write(u"\u001b[" + shift_carret + "A")

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
