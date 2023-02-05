import math
import json
import numpy as np
from matplotlib import pyplot as plt


def sinus(x, amplitude, frequency):
    """
    returns the absolute sinus of x
    :param x: tile index
    :param amplitude: [0,9999]
    :param frequency:
    :return:
    """
    if amplitude > 9999:
        raise ValueError('amplitude must be smaller than 10000 or visualization will be broken')

    return abs(round(amplitude * math.sin(frequency * x)))


def sinus_half(x, amplitude, frequency):
    """
    returns the sinus of x with a half period of 0
    :param x: tile index
    :param amplitude: [0,9999]
    :param frequency:
    :return:
    """
    if amplitude > 9999:
        raise ValueError('amplitude must be smaller than 10000 or visualization will be broken')

    return max(round(amplitude * math.sin(frequency * x)), 0)


def constant_speed(x, number):
    """
    returns a constant speed limit for all tiles
    :param x: tile index
    :param number:
    :return:
    """
    return number


def step_function(x, amplitude, frequency):
    """
    returns the curvature of a sinus as a step function
    :param x:
    :param amplitude:
    :param frequency:
    :return:
    """
    if amplitude > 9999:
        raise ValueError('amplitude must be smaller than 10000 or visualization will be broken')

    value = amplitude * math.sin(frequency * x)
    if value > 0:
        return amplitude
    elif value <= 0:
        return 0

def contract_function(x):
    """
    returns a function where at the beginning there is a strong curve than no curvature at all to
    simulate an escape-velocity of the leader.
    Hint: The breakpoint is hard coded due to time constraints.
    :param x:
    :return:
    """
    if x < 50:
        return 2000
    else:
        return 0


def step_function_twice(x, amplitude, frequency):
    """
    DO NOT USE! Does not work as intended.
    returns the curvature of an asymmetric sinus like step function according to a fourier series
    https://www.max-academy.de/contentPlayer/60bdf0ffbf5215007a86d933/606ea3c5d6a1480064c6c94e
    https://www.elektroniktutor.de/fachmathematik/fourier.html
    :param x:
    :param amplitude:
    :param frequency: Grundfrequenz
    :return:
    """
    w = 2 * math.pi / frequency
    a0 = amplitude
    value = a0 / 2 + \
            0.7484 * math.sin(1 * w * x + np.arctan(0.4399 / 0.6055)) + \
            0.6054 * math.sin(2 * w * x + np.arctan(0.5758 / 0.1871)) + \
            0.4036 * math.sin(3 * w * x + np.arctan(0.3839 / -0.1247)) + \
            0.1871 * math.sin(4 * w * x + np.arctan(0.1100 / -0.1514)) + \
            0.1247 * math.sin(6 * w * x + np.arctan(0.0733 / 0.1009)) + \
            0.1730 * math.sin(7 * w * x + np.arctan(0.1645 / 0.0535)) + \
            0.1514 * math.sin(8 * w * x + np.arctan(0.1440 / -0.0468)) + \
            0.0832 * math.sin(9 * w * x + np.arctan(0.0489 / -0.0673))
    '''
    A = amplitude
    A0 = 4 * A
    A1 = 6.62 * frequency
    A2 = 3.31 * frequency
    A3 = 0
    A4 = -1.65 * frequency
    w = 2 * math.pi / frequency

    value = A0 + A1 * math.cos(w * x) + A2 * math.cos(2 * w * x) + A3 * math.cos(3 * w * x) + A4 * math.cos(4 * w * x)
    '''
    return value


class TileAttributeSetter:

    def __init__(self, sim, cfg, modus='sinus', generate=True, amplitude=5, frequency=0.2, constant_curvature=5):
        self.simulation = sim
        self.cfg = cfg
        self.tiles = sim.get_tiles()
        self.modus = modus
        self.attr_dict = None

        if generate:
            self.generate_attr_dict(amplitude=amplitude, frequency=frequency, constant_curvature=constant_curvature)
            self.save_attr_dict()
        else:
            try:
                self.load_attr_dict()
            except FileNotFoundError as e:
                print(e)

    def generate_attr_dict(self, amplitude, frequency, constant_curvature):
        """
        generates a dictionary with the curvature or beauty values for each tile and set the values for the tiles
        Each section have the same curvature and beauty value
        First value is the curvature
        Second value the maximum allowed speed
        Third value is the beauty
        :param constant_curvature: value if all curves should be constant. Only for modus constant speed
        :param amplitude: for sinus like curvatures
        :param frequency: for sinus like curvatures
        :return:
        """
        attr_dict = dict()

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

            elif self.modus == 'constant':
                attr = constant_speed(index, constant_curvature)
                attr_list.append(attr)

            elif self.modus == 'step_function':
                attr = step_function(index, amplitude, frequency)
                attr_list.append(attr)

            elif self.modus == 'contract_function':
                attr = contract_function(index)
                attr_list.append(attr)

            else:
                attr = 0
                attr_list.append(attr)

            # Second value is the speed limit depending on curvature
            attr_list.append(self.curve_speed_limit(attr_list[0]))

            # Third value is the beauty from the default value in tile
            attr_list.append(section[0].get_beauty())

            # set the values for the tiles according to attr_list
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
        with open('./StreetAttributes/attr_list.json', 'w') as f:
            json.dump(self.attr_dict, f)

    def load_attr_dict(self):
        """
        loads the attr_dict from a json file.
        First value is the curvature
        Second value the maximum allowed speed
        Third value is the beauty
        :return:
        """
        with open('./StreetAttributes/'
                  'attr_list.json', 'r') as f:
            self.attr_dict = json.load(f)

        for key, value in self.attr_dict.items():
            for lane in range(0, self.simulation.get_lanes() + 1):
                # first value is the curvature
                # if no curvature is set in the json file, the curvature will be the minimum value
                if type(value[0]) is int:
                    self.tiles[int(key)][lane].set_curvature(value[0])
                else:
                    self.tiles[int(key)][lane].set_curvature(0)
                # second value is the speed limit
                # if no speed limit is set in the json file, the speed limit will be calculated from the curvature
                # if no curvature is set in the json file, the speed limit will be the maximum value
                if type(value[1]) is int:
                    if value[1] == 0:
                        raise ValueError('Speed limit must be greater than 0')
                    else:
                        self.tiles[int(key)][lane].set_speed_limit(value[1])
                else:
                    speed_limit = self.curve_speed_limit(self.tiles[int(key)][lane].get_curvature())
                    self.tiles[int(key)][lane].set_speed_limit(speed_limit)
                # third value is the beauty
                # if no beauty is set in the json file, the beauty will be the minimum value
                if type(value[2]) is int:
                    self.tiles[int(key)][lane].set_beauty(value[2])
                else:
                    self.tiles[int(key)][lane].set_beauty(0)

    def curve_speed_limit(self, curve):
        """
        This function creates a custom speed limit dict for each curvature value
        maximum curvature is 10000[ce]/100[km/h] = 100[ce / km/h]
        curvature data see https://roadcurvature.com/
        :return:
        """
        speedlimit_to_curvature = self.cfg.speedlimit_to_curvature
        if curve not in range(0, 10000):
            raise ValueError("Curve value not in range [0, 10000]", curve)

        for max_speed in speedlimit_to_curvature:
            if curve in range(*speedlimit_to_curvature[max_speed]):
                return max_speed

    def get_attr_dict(self):
        return self.attr_dict


if __name__ == '__main__':
    # 100 linearly spaced numbers
    x = np.linspace(-10, 10, 100)
    vectorized_fct = np.vectorize(step_function)
    plt.plot(x, vectorized_fct(x, 510, 1))
    plt.show()
