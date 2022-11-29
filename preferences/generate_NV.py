import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress


def normal_dist(x, mean, sd):
    prob_density = (np.pi * sd) * np.exp(-0.5 * ((x - mean) / sd) ** 2)
    return prob_density


def calc_slope(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)


def main():
    # Calculate mean and Standard deviation.
    x = np.linspace(1, 50, 200)
    mean = np.mean(x)
    sd = np.std(x)

    # Apply function to the data.
    pdf = normal_dist(x, mean, sd)

    # Plotting the Results
    plt.plot(x, pdf, color='red')
    plt.xlabel('Data points')
    plt.ylabel('Probability Density')
    plt.title('Normal Distribution')
    plt.show()


if __name__ == '__main__':
    main()
