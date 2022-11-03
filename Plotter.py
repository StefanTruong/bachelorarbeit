from AnalyzerSingleSim import *
import matplotlib.pyplot as plt
import numpy as np


def flow_density_diagram(density_list, avg_flow_list, std_flow_list):
    plt.errorbar(density_list, avg_flow_list, xerr=0, yerr=1.96 * np.array(std_flow_list))
    plt.title('Fundamental Diagram')
    plt.xlabel('Vehicle Density [Vehicles per site]')
    plt.ylabel('Flow [Vehicles per time step]')
    plt.show()


