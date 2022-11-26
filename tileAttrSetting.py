import math
import json


def sinus(x, amplitude=2000, frequency=0.1):
    """
    returns the absolute sinus of x
    :param x:
    :param amplitude: [0,9999]
    :param frequency:
    :return:
    """
    if amplitude > 9999:
        raise ValueError('amplitude must be smaller than 10000 or visualization will be broken')

    return abs(round(amplitude * math.sin(frequency * x)))


def sinus_half(x, amplitude=2000, frequency=0.1):
    """
    returns the sinus of x with a half period of 0
    :param x:
    :param amplitude: [0,9999]
    :param frequency:
    :return:
    """
    if amplitude > 9999:
        raise ValueError('amplitude must be smaller than 10000 or visualization will be broken')

    return max(round(amplitude * math.sin(frequency * x)), 0)


class TileAttributeSetter:

    def __init__(self, simulation, modus='sinus', generate=True, amplitude=5, frequency=0.2):
        self.simulation = simulation
        self.tiles = simulation.get_tiles()
        self.modus = modus
        self.attr_dict = None

        if generate:
            self.generate_attr_dict(amplitude=amplitude, frequency=frequency)
            self.save_attr_dict()
        else:
            try:
                self.load_attr_dict()
            except FileNotFoundError as e:
                print(e)

    def generate_attr_dict(self, amplitude, frequency):
        """
        generates a dictionary with the curvature or beauty values for each tile and set the values for the tiles
        Each section have the same curvature and beauty value
        First value is the curvature
        Second value the maximum allowed speed
        Third value is the beauty
        :param amplitude:
        :param frequency:
        :return:
        """
        attr_dict = dict()
        # Unlimited speed limit is default value. To Change it go to tile class
        max_speed = self.tiles[0][0].get_speed_limit()
        # beauty default value is zero
        initial_beauty = 0

        for section in self.tiles:
            attr_list = []
            index = section[0].get_index()

            # First value is the curvature
            # generate sinus curve
            if self.modus == 'sinus':
                attr = sinus(index, amplitude, frequency)
                attr_list.append(attr)

            # generate half sinus curve
            elif self.modus == 'sinus_half':
                attr = sinus_half(index, amplitude, frequency)
                attr_list.append(attr)

            else:
                attr = 0
                attr_list.append(attr)

            # Second value is the speed limit
            attr_list.append(max_speed)

            # Third value is the beauty
            attr_list.append(initial_beauty)

            for lane in range(0, self.simulation.get_lanes() + 1):
                # first value is the curvature
                section[lane].set_curvature(attr_list[0])
                # Second value the maximum allowed speed
                section[lane].set_speed_limit(attr_list[1])
                # Third value is the beauty
                section[lane].set_beauty(attr_list[2])

            attr_dict[index] = attr_list

        self.attr_dict = attr_dict

    def save_attr_dict(self):
        """
        saves the attr_dict as a json file. The json file contains the curvature and beauty values for each section
        not tile!!!
        :return:
        """
        with open('./Street Attributes/attr_list.json', 'w') as f:
            json.dump(self.attr_dict, f)

    def load_attr_dict(self):
        """
        loads the attr_dict from a json file.
        First value is the curvature
        Second value the maximum allowed speed
        Third value is the beauty
        :return:
        """
        with open('./Street Attributes/attr_list.json', 'r') as f:
            attr_dict = json.load(f)

        for key, value in attr_dict.items():
            for lane in range(0, self.simulation.get_lanes() + 1):
                # first value is the curvature
                self.tiles[int(key)][lane].set_curvature(value[0])
                # second value is the speed limit
                self.tiles[int(key)][lane].set_speed_limit(value[1])
                # third value is the beauty
                self.tiles[int(key)][lane].set_beauty(value[2])
