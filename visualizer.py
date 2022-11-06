from tile import *
from vehicles import *
import numpy as np
import time, sys, random


class VisualizeStreet:

    def __init__(self, simulation):
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

    def traffic_vis_tiles_granular(self):
        """
        simply plots the street with the vehicles on it
        :return:
        """
        for lane in range(0, self.simulation.num_lanes + 1):
            visual = ''
            for tile in self.simulation.tiles:
                visual += tile[lane].get_icon_granular()
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
