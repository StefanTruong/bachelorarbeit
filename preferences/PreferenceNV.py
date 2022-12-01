import json

import numpy as np
import matplotlib.pyplot as plt
import math


def plot_nv(pref_range, pdf, label='Missing Label'):
    plt.plot(pref_range, pdf, color='red')
    plt.xlabel(label)
    plt.ylabel('Probability Density')
    plt.title('Normal Distribution')
    plt.show()


def plot_linear_combination(dist_preference_sight, first_dist, second_dist=None, mixed_dist=None):
    """
    plot linear combination of two preference distributions which are linear combinations of NV
    :param dist_preference_sight:
    :param first_dist:
    :param second_dist:
    :param mixed_dist:
    :return:
    """
    plt.plot(dist_preference_sight, first_dist, color='red', label='first')
    if second_dist is not None:
        plt.plot(dist_preference_sight, second_dist, color='blue', label='second')
    if mixed_dist is not None:
        plt.plot(dist_preference_sight, mixed_dist, color='green', label='mixed')
    plt.legend()
    plt.show()


def normal_dist(values, mean, sd, amp=1):
    """
    calculate normal distribution matching the values list length
    :param amp: amplitude of NV to strengthen preference
    :param values: list of sight distance values to be plotted
    :param mean: mean of the preference
    :param sd: standard deviation of the preference
    :return: list of normal distribution values matching the values list length
    """
    prob_density = []
    for x in values:
        var = float(sd) ** 2
        denominator = (2 * math.pi * var) ** .5
        num = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
        prob_density.append(amp * (num / denominator))

    return prob_density


def calc_gradient(pdf, dist_preference_range):
    """
    calculate gradient sign for distance given a preference distribution
    :param pdf: probability density function
    :param dist_preference_range: range of distance preference
    :return:
    """
    start = int(dist_preference_range[0])
    end = int(dist_preference_range[-1])

    gradient = np.gradient(pdf)
    gradient_sign = []
    for i in range(start, end):
        if gradient[i] >= 0:
            sign = 1
        else:
            sign = -1
        gradient_sign.append(sign)
    return gradient_sign


def save_dict(dictionary):
    with open('data.json', 'w') as fp:
        json.dump(dictionary, fp, indent=4)


class Preferences:
    def __init__(self):
        # distance preference single sided
        self.dist_mean_small = 6
        self.dist_sd_small = 1
        self.dist_ampl_small = 1
        self.dist_mean_avg = 8
        self.dist_sd_avg = 1
        self.dist_ampl_avg = 1
        self.dist_mean_high = 10
        self.dist_sd_high = 1
        self.dist_ampl_high = 1

        # curve speed preference
        self.curve_preference_cautious = None  # ToDo Input parameter
        self.curve_preference_average = None  # ToDo Input parameter
        self.curve_preference_speed = None  # ToDo Input parameter
        self.curve_sd_cautious = 1
        self.curve_ampl_cautious = 1
        self.curve_sd_average = 1
        self.curve_ampl_average = 1
        self.curve_sd_speed = 1
        self.curve_ampl_speed = 1

        # summarized preferences for dist and curve_speed
        # dist_preference_all = {'small':   {pdf: dist_preference_small,
        #                                   mean: mean,
        #                                   sd: sd, ampl: ampl},
        #                        'small_small': ...}
        # curve_preference_all = {'speed' :    {velo1: {range: range(), pdf: pdf, mean: mean, sd: sd, ampl: ampl},
        #                                       velo2: ...,
        #                         'average': ...
        # speed_gap_preferences = {'speed': {'small': {velo1: {pdf: merged_pdf, range: range, gradient: gradient}}}}
        self.dist_preference_all = None
        self.curve_preference_all = None
        self.speed_gap_preferences = None

        # How far the NV should be calculated and plotted
        dist_preference_sight = np.linspace(0, 100, 500)

        # plot preference distribution
        # self.plot_distance_preferences(dist_preference_sight)

        # calculate pdf for single distance preference used for leader or sweeper
        # calculate pdf for mixed distance preference used for inbetween vehicles
        self.calc_distance_pdf(dist_preference_sight)

        # calculate pdf for speed-curvature preference
        self.calc_curvature_pdf(dist_preference_sight)

        # merge curvature-speed preference and distance preference
        self.calc_merged_preference(dist_preference_sight)

        # check linear combination of pdfs

        #plot_linear_combination(dist_preference_sight, self.dist_preference_all['small_small']['pdf'],
        #                        self.curve_preference_all['cautious'][5]['pdf'], self.speed_gap_preferences['cautious']['small_small'][5]['pdf'])
        print(self.dist_preference_all['small_small']['mean'])
        print(self.curve_preference_all['cautious'][5]['mean'])
        print(len(self.speed_gap_preferences['cautious']['small_small'][5]['pdf']))
        print(len(self.speed_gap_preferences['cautious']['small_small'][5]['gradient']))


    def plot_distance_preferences(self, dist_preference_sight):
        """
        calculates the distance preference for small, avg and high for velocity adjustments
        depending on vehicle distance
        :return: a list of [1, 1, 1, 1, 1, -1, -1, -1, -1, -1]. Index indicates how velocity should be adjusted
        """
        # calculate y-values and plot NV for each preference
        pdf_small = normal_dist(dist_preference_sight, self.dist_mean_small, self.dist_sd_small, self.dist_ampl_small)
        pdf_avg = normal_dist(dist_preference_sight, self.dist_mean_avg, self.dist_sd_avg, self.dist_ampl_avg)
        pdf_high = normal_dist(dist_preference_sight, self.dist_mean_high, self.dist_sd_high, self.dist_ampl_high)

        plt.plot(dist_preference_sight, pdf_small, color='red', label='small')
        plt.plot(dist_preference_sight, pdf_avg, color='blue', label='avg')
        plt.plot(dist_preference_sight, pdf_high, color='green', label='high')
        plt.xlabel('Vehicle Distance')
        plt.ylabel('Density')
        plt.title('Distance Preference Distribution')
        plt.legend()
        plt.show()

    def calc_distance_pdf(self, dist_preference_sight):
        """
        calculates the distance pdf for small, avg and high for velocity adjustments for leader and sweeper
        calculates the distance pdf for small, avg and high for velocity adjustments inbetween vehicles
        :param dist_preference_sight:
        :return:
        """
        # calculate y-values for each onesided preference
        pdf_small = normal_dist(dist_preference_sight, self.dist_mean_small, self.dist_sd_small, self.dist_ampl_small)
        pdf_avg = normal_dist(dist_preference_sight, self.dist_mean_avg, self.dist_sd_avg, self.dist_ampl_avg)
        pdf_high = normal_dist(dist_preference_sight, self.dist_mean_high, self.dist_sd_high, self.dist_ampl_high)

        # Linear combination of normal distributed Variables N(a*mean1 + b*mean2, sqrt(a²sd1² + b²sd2²))
        # calculate mean and sd for each mixed preference
        mean_small_small = self.dist_ampl_small * self.dist_mean_small - self.dist_ampl_small * self.dist_mean_small
        sd_small_small = math.sqrt((self.dist_ampl_small ** 2 * self.dist_sd_small ** 2) +
                                   (self.dist_ampl_small ** 2 * self.dist_sd_small ** 2))

        mean_small_avg = self.dist_ampl_small * self.dist_mean_small - self.dist_ampl_avg * self.dist_mean_avg
        sd_small_avg = math.sqrt((self.dist_ampl_small ** 2 * self.dist_sd_small ** 2) +
                                 (self.dist_ampl_avg ** 2 * self.dist_sd_avg ** 2))

        mean_small_high = self.dist_ampl_small * self.dist_mean_small - self.dist_ampl_high * self.dist_mean_high
        sd_small_high = math.sqrt((self.dist_ampl_small ** 2 * self.dist_sd_small ** 2) +
                                  (self.dist_ampl_high ** 2 * self.dist_sd_high ** 2))

        mean_avg_avg = self.dist_ampl_avg * self.dist_mean_avg - self.dist_ampl_avg * self.dist_mean_avg
        sd_avg_avg = math.sqrt((self.dist_ampl_avg ** 2 * self.dist_sd_avg ** 2) +
                               (self.dist_ampl_avg ** 2 * self.dist_sd_avg ** 2))

        mean_avg_high = self.dist_ampl_avg * self.dist_mean_avg - self.dist_ampl_high * self.dist_mean_high
        sd_avg_high = math.sqrt((self.dist_ampl_avg ** 2 * self.dist_sd_avg ** 2) +
                                (self.dist_ampl_high ** 2 * self.dist_sd_high ** 2))

        mean_high_high = self.dist_ampl_high * self.dist_mean_high - self.dist_ampl_high * self.dist_mean_high
        sd_high_high = math.sqrt((self.dist_ampl_high ** 2 * self.dist_sd_high ** 2) +
                                 (self.dist_ampl_high ** 2 * self.dist_sd_high ** 2))

        # calculate y-values for each preference
        pdf_small_small = normal_dist(dist_preference_sight, mean_small_small, sd_small_small)
        pdf_small_avg = normal_dist(dist_preference_sight, mean_small_avg, sd_small_avg)
        pdf_small_high = normal_dist(dist_preference_sight, mean_small_high, sd_small_high)
        pdf_avg_avg = normal_dist(dist_preference_sight, mean_avg_avg, sd_avg_avg)
        pdf_avg_high = normal_dist(dist_preference_sight, mean_avg_high, sd_avg_high)
        pdf_high_high = normal_dist(dist_preference_sight, mean_high_high, sd_high_high)

        self.dist_preference_all = {
            'small': {'pdf': pdf_small, 'mean': self.dist_mean_small, 'sd': self.dist_sd_small,
                      'ampl': self.dist_ampl_small},
            'avg': {'pdf': pdf_avg, 'mean': self.dist_mean_avg, 'sd': self.dist_sd_avg, 'ampl': self.dist_ampl_avg},
            'high': {'pdf': pdf_high, 'mean': self.dist_mean_high, 'sd': self.dist_sd_high,
                     'ampl': self.dist_ampl_high},
            'small_small': {'pdf': pdf_small_small, 'mean': mean_small_small, 'sd': sd_small_small},
            'small_avg': {'pdf': pdf_small_avg, 'mean': mean_small_avg, 'sd': sd_small_avg},
            'small_high': {'pdf': pdf_small_high, 'mean': mean_small_high, 'sd': sd_small_high},
            'avg_avg': {'pdf': pdf_avg_avg, 'mean': mean_avg_avg, 'sd': sd_avg_avg},
            'avg_high': {'pdf': pdf_avg_high, 'mean': mean_avg_high, 'sd': sd_avg_high},
            'high_high': {'pdf': pdf_high_high, 'mean': mean_high_high, 'sd': sd_high_high}
        }

    def calc_curvature_pdf(self, dist_preference_sight):
        """
        calculates the preferred speed pdf for each curvature range. Should correspond to speedlimit_to_curvature dict
        :return:    curve_preference = {'speed' :   {velo1: {range: range(), pdf: pdf, mean: mean, sd: sd, ampl: ampl},
                                        'average': ...
        """
        # From tileAttrSetting.py curve-speed-limit
        speedlimit_to_curvature = {
            10: (0, 500),  # 10tiles ~ 40 m/s ~ 144 km/h
            9: (500, 800),  # 9 tiles ~ 36 m/s ~ 129 km/h
            8: (800, 1000),  # 8 tiles ~ 32 m/s ~ 115 km/h
            7: (1000, 1200),  # 7 tiles ~ 28 m/s ~ 101 km/h
            6: (1200, 1400),  # 6 tiles ~ 24 m/s ~ 86 km/h
            5: (1400, 1600),  # 5 tiles ~ 20 m/s ~ 72 km/h
            4: (1600, 1800),  # 4 tiles ~ 16 m/s ~ 57 km/h
            3: (1800, 2000),  # 3 tiles ~ 12 m/s ~ 43 km/h
            2: (2000, 3000),  # 2 tiles ~ 8 m/s ~ 29 km/h
            1: (3000, 10000),  # 1 tile ~ 4 m/s ~ 14 km/h
        }
        # The speed type wants to ride maximum speed
        self.curve_preference_speed = speedlimit_to_curvature

        # The average type wants to ride one speed less
        self.curve_preference_average = {
            9: (0, 500),
            8: (500, 800),
            7: (800, 1000),
            6: (1000, 1200),
            5: (1200, 1400),
            4: (1400, 1600),
            3: (1600, 1800),
            2: (1800, 3000),
            1: (3000, 10000),
        }

        # The cautious type wants to ride two speed less
        self.curve_preference_cautious = {
            8: (0, 500),
            7: (500, 800),
            6: (800, 1000),
            5: (1000, 1200),
            4: (1200, 1400),
            3: (1400, 1600),
            2: (1600, 3000),
            1: (3000, 10000),
        }

        # generates a dictionary in dictionary for each speed cto curvature preference
        self.curve_preference_all = {'speed': {}, 'average': {}, 'cautious': {}}
        for velo, curve_range in self.curve_preference_speed.items():
            mean = int(velo)
            sd_speed = self.curve_sd_speed
            ampl_speed = self.curve_ampl_speed
            pdf = normal_dist(dist_preference_sight, mean, sd_speed, ampl_speed)
            self.curve_preference_all['speed'][velo] = {'range': curve_range,
                                                        'pdf': pdf,
                                                        'mean': mean, 'sd': sd_speed, 'ampl': ampl_speed}

        for velo, curve_range in self.curve_preference_average.items():
            mean = int(velo)
            sd_average = self.curve_sd_average
            ampl_average = self.curve_ampl_average
            pdf = curve_range, normal_dist(dist_preference_sight, mean, sd_average, ampl_average)
            self.curve_preference_all['average'][velo] = {'range': curve_range,
                                                          'pdf': pdf,
                                                          'mean': mean, 'sd': sd_average, 'ampl': ampl_average}

        for velo, curve_range in self.curve_preference_cautious.items():
            mean = int(velo)
            sd_cautious = self.curve_sd_cautious
            ampl_cautious = self.curve_ampl_cautious
            pdf = normal_dist(dist_preference_sight, mean, sd_cautious, ampl_cautious)
            self.curve_preference_all['cautious'][velo] = {'range': curve_range,
                                                           'pdf': pdf,
                                                           'mean': mean, 'sd': sd_cautious, 'ampl': ampl_cautious}

    def calc_merged_preference(self, dist_preference_sight):
        """
        merges the preferences of curvature-speed preference and distance preference
        :param dist_preference_sight:
        :return: dict which shows how a vehicle should accelerate according to its preference
                 = {'speed':  {'small':   {velocity1:  {pdf: merged_pdf, range: range(), gradient: gradient},
                                            velocity2:  {pdf: merged_pdf, range: range()], gradient: gradient},
                                 'avg':     ...                              },

                    'average':  ...}
        """

        # What preferences are available
        speed_preferences = ['speed', 'average', 'cautious']
        gap_preferences = \
            ['small', 'avg', 'high', 'small_small', 'small_avg', 'small_high', 'avg_avg', 'avg_high', 'high_high']
        speed_gap_preferences = {}

        for speed_preference in speed_preferences:
            speed_gap_preferences[speed_preference] = {}

            for gap_preference in gap_preferences:
                speed_gap_preferences[speed_preference][gap_preference] = {}

                for velo, values in self.curve_preference_all[speed_preference].items():
                    # Hint: not all dist preferences has an amplitude e.g. small_small.
                    # Relative importance of speed and distance preference are set equal
                    # dist_preference_all =
                    # {'small': {pdf: dist_preference_small, mean: mean, sd: sd, ampl: ampl}, ..., 'small_small': ...}

                    # curve_preference_all =
                    # {'speed' :   {velo1: {range: range(), pdf: pdf, mean: mean, sd: sd, ampl: ampl},
                    #               velo2: {range: range(), pdf: pdf, mean: mean, sd: sd, ampl: ampl}},
                    #  'average': ...

                    merged_mean = self.curve_preference_all[speed_preference][velo]['mean'] + \
                                  self.dist_preference_all[gap_preference]['mean']
                    merged_sd = math.sqrt(self.curve_preference_all[speed_preference][velo]['sd'] ** 2 +
                                          self.dist_preference_all[gap_preference]['sd'] ** 2)

                    merged_pdf = normal_dist(dist_preference_sight, merged_mean, merged_sd)
                    gradient = calc_gradient(merged_pdf, dist_preference_sight)
                    speed_gap_preferences[speed_preference][gap_preference][velo] = \
                        {'pdf': merged_pdf, 'range': values['range'], 'gradient': gradient}

        self.speed_gap_preferences = speed_gap_preferences
        save_dict(self.speed_gap_preferences)


if __name__ == '__main__':
    distance_preferences = Preferences()
