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

        self.dist_preference_small_small = None
        self.dist_preference_small_avg = None
        self.dist_preference_small_high = None
        self.dist_preference_avg_avg = None
        self.dist_preference_avg_high = None
        self.dist_preference_high_high = None

        # How far the NV should be calculated and plotted
        dist_preference_sight = np.linspace(0, 50, 500)

        # plot preference distribution
        # self.plot_distance_preferences(dist_preference_sight)

        # calculate pdf for single distance preference used for leader or sweeper
        self.calc_pdf_oneside(dist_preference_sight)

        # calculate pdf for mixed distance preference used for inbetween vehicles
        self.calc_pdf_twoside(dist_preference_sight)

        # check linear combination of pdfs
        plot_linear_combination(dist_preference_sight, self.dist_preference_avg, self.dist_preference_high,
                                self.dist_preference_avg_high)

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

    def calc_pdf_oneside(self, dist_preference_sight):
        """
        calculates the distance pdf for small, avg and high for velocity adjustments for leader and sweeper
        :param dist_preference_sight:
        :return:
        """
        # calculate y-values for each preference
        pdf_small = normal_dist(dist_preference_sight, self.dist_mean_small, self.dist_sd_small, self.dist_ampl_small)
        pdf_avg = normal_dist(dist_preference_sight, self.dist_mean_avg, self.dist_sd_avg, self.dist_ampl_avg)
        pdf_high = normal_dist(dist_preference_sight, self.dist_mean_high, self.dist_sd_high, self.dist_ampl_high)

        self.dist_preference_small = pdf_small
        self.dist_preference_avg = pdf_avg
        self.dist_preference_high = pdf_high

    def calc_pdf_twoside(self, dist_preference_sight):
        """
        calculates the distance pdf for small, avg and high for velocity adjustments inbetween vehicles
        :param dist_preference_sight:
        :return:
        """
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


if __name__ == '__main__':
    distance_preferences = Preferences()
