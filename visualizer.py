from tile import *
import numpy as np
import sys


def traffic_vis_tiles_step_by_step(simulation):
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
    sys.stdout.write('\n')



