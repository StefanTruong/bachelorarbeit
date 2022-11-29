import numpy as np
import matplotlib.pyplot as plt
import math


def distance_preference(pref):
    """
    get distance preference range from [0, max] with max steps
    :param pref: String. high, medium, low. Has to begin with 0
    :return:
    """
    # preference for distance
    preference_range = []

    if pref == 'small':
        preference_range = np.linspace(0, 10, 10)
    elif pref == 'avg':
        preference_range = np.linspace(0, 12, 12)
    elif pref == 'high':
        preference_range = np.linspace(0, 14, 14)
    else:
        raise ValueError('pref must be avg, small or high')

    return preference_range


def normal_dist(values, mean, sd):
    """
    calculate normal distribution
    :param values:
    :param mean:
    :param sd:
    :return:
    """
    prob_density = []
    for x in values:
        var = float(sd) ** 2
        denominator = (2 * math.pi * var) ** .5
        num = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
        prob_density.append(num / denominator)

    return prob_density


def calc_gradient_sign(pdf, dist_preference_range, dist=None):
    """
    calculate gradient sign for distance given a preference distribution
    :param pdf: probability density function
    :param dist: Integer. distance value to get gradient
    :param dist_preference_range: range of distance preference
    :return:
    """

    start = int(dist_preference_range[0])
    end = int(dist_preference_range[-1])

    if dist is not None:
        if dist in range(start, end):
            gradient = np.gradient(pdf)
        else:
            raise ValueError('dist must be in range of dist_preference_range')

        if gradient[dist] >= 0:
            sign = 1
        else:
            sign = -1
        return gradient[dist]

    else:
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
        self.dist_preference_avg = None
        self.dist_preference_high = None

        self.calculate_preferences()

    def calculate_preferences(self):
        """
        calculates the distance preference for small, avg and high for velocity adjustments
        [1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
        :return:
        """
        # What preference modi are available see def distance_preference
        dist_preference_modi = ['small', 'avg', 'high']

        # calculate distance preference for each modi and save it in a list within a dictionary
        my_pref_dist_dict = {}
        for modus in dist_preference_modi:
            my_pref_dist_dict[f'dist_preference_{modus}'] = distance_preference(modus)

        for key, pref_range in my_pref_dist_dict.items():
            mean = np.mean(pref_range)
            sd = np.std(pref_range)
            pdf = normal_dist(pref_range, mean, sd)
            gradient_sign = calc_gradient_sign(pdf, pref_range)
            my_pref_dist_dict[key] = gradient_sign

            # print(pdf)
            # print(gradient_sign)
            # print(sum(pdf))

            # plt.plot(pref_range, pdf, color='red')
            # plt.xlabel('Data points')
            # plt.ylabel('Probability Density')
            # plt.title('Normal Distribution')
            # plt.show()

        # save preferences in class
        self.dist_preference_small = my_pref_dist_dict['dist_preference_small']
        self.dist_preference_avg = my_pref_dist_dict['dist_preference_avg']
        self.dist_preference_high = my_pref_dist_dict['dist_preference_high']

        # print(vars(self))


if __name__ == '__main__':
    # main()
    distance_preferences = Preferences()
