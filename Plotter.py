from AnalyzerSingleSim import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


def flow_density_diagram_errorbar(density_list, avg_flow_list, std_flow_list):
    plt.errorbar(density_list, avg_flow_list, xerr=0, yerr=1.96 * np.array(std_flow_list))
    plt.title('Fundamental Diagram')
    plt.xlabel('Vehicle Density [vehicles per site]')
    plt.ylabel('Flow [vehicles per time step]')
    plt.show()
    print(avg_flow_list)


def flow_density_diagram_textbook(density_list, avg_flow_list):
    """
    ToDo since not tested if finished
    :param density_list:
    :param avg_flow_list:
    :return:
    """
    plt.plot(density_list, avg_flow_list)
    plt.title('Standard Fundamental Diagram')
    plt.xlabel('Vehicle Density [vehicles per site]')
    plt.ylabel('Flow [vehicles per time step]')
    plt.show()
    print(avg_flow_list)


def time_space_granular(data):
    """
    Plots a 2D Pixel Plot
    :param data: list of lists representing the space in x-axis and the time in the y-axis
    :return:
    """
    # data is list of list and have to be converted to a numpy matrix for plotting
    np_array = np.array(data)
    np_matrix = np.asmatrix(np_array)

    fig = plt.figure()
    fig.suptitle('Space Time Plot', fontsize=12)

    ax = fig.add_subplot(111)
    ax.imshow(np_matrix, cmap=plt.cm.gray,
              interpolation='nearest')

    ax.set_xlabel("Space")
    ax.set_ylabel("Time")
    plt.show()
