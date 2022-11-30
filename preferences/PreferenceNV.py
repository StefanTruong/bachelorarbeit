import numpy as np
import matplotlib.pyplot as plt
import math


def plot_nv(pref_range, pdf, label='Missing Label'):
    plt.plot(pref_range, pdf, color='red')
    plt.xlabel(label)
    plt.ylabel('Probability Density')
    plt.title('Normal Distribution')
    plt.show()


def plot_linear_combination(dist_preference_sight, first_dist, second_dist, mixed_dist):
    """
    plot linear combination of two preference distributions which are linear combinations of NV
    :param dist_preference_sight:
    :param first_dist:
    :param second_dist:
    :param mixed_dist:
    :return:
    """
    plt.plot(dist_preference_sight, first_dist, color='red', label='first')
    plt.plot(dist_preference_sight, second_dist, color='blue', label='second')
    plt.plot(dist_preference_sight, mixed_dist, color='green', label='mixed')
    plt.legend()
    plt.show()


def normal_dist(values, mean, sd, amp=1):
    """
    calculate normal distribution
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


def calc_gradient_sign(pdf, dist_preference_range):
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


class Preferences:
    def __init__(self):
        # distance preference single sided
        self.dist_preference_small = None
        self.dist_mean_small = 6
        self.dist_sd_small = 1
        self.dist_ampl_small = 1
        self.dist_preference_avg = None
        self.dist_mean_avg = 8
        self.dist_sd_avg = 1
        self.dist_ampl_avg = 1
        self.dist_preference_high = None
        self.dist_mean_high = 10
        self.dist_sd_high = 1
        self.dist_ampl_high = 1

        # distance preference double sided
        self.dist_preference_small_small = None
        self.dist_preference_small_avg = None
        self.dist_preference_small_high = None
        self.dist_preference_avg_avg = None
        self.dist_preference_avg_high = None
        self.dist_preference_high_high = None

        # curve speed preference
        self.curve_preference_all = None
        self.curve_preference_cautious = None
        self.curve_sd_cautious = 1
        self.curve_ampl_cautious = 1
        self.curve_preference_average = None
        self.curve_sd_average = 1
        self.curve_ampl_average = 1
        self.curve_preference_speed = None
        self.curve_sd_speed = 1
        self.curve_ampl_speed = 1

        # How far the NV should be calculated and plotted
        dist_preference_sight = np.linspace(0, 100, 500)

        # plot preference distribution
        # self.plot_distance_preferences(dist_preference_sight)

        # calculate pdf for single distance preference used for leader or sweeper
        # calculate pdf for mixed distance preference used for inbetween vehicles
        self.calc_distance_pdf(dist_preference_sight)

        # check linear combination of pdfs
        # plot_linear_combination(dist_preference_sight, self.dist_preference_avg, self.dist_preference_high,
        #                          self.dist_preference_avg_high)

        # calculate pdf for speed-curvature preference
        self.calc_curvature_pdf(dist_preference_sight)

        # calculate gradient sign for each distance preference
        # ToDo

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

        self.dist_preference_small = pdf_small
        self.dist_preference_avg = pdf_avg
        self.dist_preference_high = pdf_high

        # Linear combination of normal distributed Variables N(a*mean1 + b*mean2, sqrt(a²sd1² + b²sd2²))
        # calculate mean and sd for each mixed preference
        mean_small_small = self.dist_ampl_small * self.dist_mean_small
        sd_small_small = math.sqrt((self.dist_ampl_small ** 2 * self.dist_sd_small ** 2) +
                                   (self.dist_ampl_small ** 2 * self.dist_sd_small ** 2))

        mean_small_avg = self.dist_ampl_small * self.dist_mean_small + self.dist_ampl_avg * self.dist_mean_avg
        sd_small_avg = math.sqrt((self.dist_ampl_small ** 2 * self.dist_sd_small ** 2) +
                                 (self.dist_ampl_avg ** 2 * self.dist_sd_avg ** 2))

        mean_small_high = self.dist_ampl_small * self.dist_mean_small + self.dist_ampl_high * self.dist_mean_high
        sd_small_high = math.sqrt((self.dist_ampl_small ** 2 * self.dist_sd_small ** 2) +
                                  (self.dist_ampl_high ** 2 * self.dist_sd_high ** 2))

        mean_avg_avg = self.dist_ampl_avg * self.dist_mean_avg
        sd_avg_avg = math.sqrt((self.dist_ampl_avg ** 2 * self.dist_sd_avg ** 2) +
                               (self.dist_ampl_avg ** 2 * self.dist_sd_avg ** 2))

        mean_avg_high = self.dist_ampl_avg * self.dist_mean_avg + self.dist_ampl_high * self.dist_mean_high
        sd_avg_high = math.sqrt((self.dist_ampl_avg ** 2 * self.dist_sd_avg ** 2) +
                                (self.dist_ampl_high ** 2 * self.dist_sd_high ** 2))

        mean_high_high = self.dist_ampl_high * self.dist_mean_high
        sd_high_high = math.sqrt((self.dist_ampl_high ** 2 * self.dist_sd_high ** 2) +
                                 (self.dist_ampl_high ** 2 * self.dist_sd_high ** 2))

        # calculate y-values for each preference
        pdf_small_small = normal_dist(dist_preference_sight, mean_small_small, sd_small_small)
        pdf_small_avg = normal_dist(dist_preference_sight, mean_small_avg, sd_small_avg)
        pdf_small_high = normal_dist(dist_preference_sight, mean_small_high, sd_small_high)
        pdf_avg_avg = normal_dist(dist_preference_sight, mean_avg_avg, sd_avg_avg)
        pdf_avg_high = normal_dist(dist_preference_sight, mean_avg_high, sd_avg_high)
        pdf_high_high = normal_dist(dist_preference_sight, mean_high_high, sd_high_high)

        self.dist_preference_small_small = pdf_small_small
        self.dist_preference_small_avg = pdf_small_avg
        self.dist_preference_small_high = pdf_small_high
        self.dist_preference_avg_avg = pdf_avg_avg
        self.dist_preference_avg_high = pdf_avg_high
        self.dist_preference_high_high = pdf_high_high

    def calc_curvature_pdf(self, dist_preference_sight):
        """
        calculates the preferred speed pdf for each curvature range. Should correspond to speedlimit_to_curvature dict
        :return:    curve_preference = {'speed' :   {velo1: [range(), pdf]
                                                    velo2: [range(), pdf]},
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
            self.curve_preference_all['speed'][velo] = [curve_range,
                                                        normal_dist(dist_preference_sight, mean, sd_speed, ampl_speed)]

        for velo, curve_range in self.curve_preference_average.items():
            mean = int(velo)
            sd_average = self.curve_sd_average
            ampl_average = self.curve_ampl_average
            self.curve_preference_all['average'][velo] = [curve_range,
                                                          normal_dist(dist_preference_sight, mean, sd_average,
                                                                      ampl_average)]

        for velo, curve_range in self.curve_preference_cautious.items():
            mean = int(velo)
            sd_cautious = self.curve_sd_cautious
            ampl_cautious = self.curve_ampl_cautious
            self.curve_preference_all['cautious'][velo] = [curve_range,
                                                           normal_dist(dist_preference_sight, mean, sd_cautious,
                                                                       ampl_cautious)]


if __name__ == '__main__':
    distance_preferences = Preferences()
