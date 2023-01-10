import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


def time_distance_diagram(summary_dict, plot_type):
    """
    Plots a time distance diagram for cars or motorcyclists according to plot_type
    :param summary_dict: result dict from AnalyzerSingleSim
    :param plot_type: Time_Distance_Diagram_Motorcyclist or Time_Distance_Diagram_Car
    :return:
    """
    adjusted_results = extractor_summary_dict(summary_dict, plot_type=plot_type)

    # if dataframe is empty e.g. no cars ot bike at all then skip plot
    if adjusted_results.empty:
        print(f'empty df for {plot_type}')
        return

    ax = adjusted_results.plot(colormap='viridis')
    ax.set_xlabel('Time')
    ax.set_ylabel('Distance')
    ax.set_title(plot_type)
    plt.show()


def velocity_distro_diagram(summary_dict, plot_type='Velocity_Distribution_Motorcyclist'):
    """

    :param summary_dict: result dict from AnalyzerSingleSim
    :param plot_type: Velocity_Distribution_Motorcyclist
    :return:
    """
    adjusted_results = extractor_summary_dict(summary_dict, plot_type=plot_type)

    # if dataframe is empty skip plot
    if adjusted_results.empty:
        print(f'empty df for {plot_type}')
        return

    # cmap = cm.ScalarMappable(cmap='rainbow')
    ax = adjusted_results.plot(kind='box', title=plot_type)
    ax.set_xlabel('Motorcyclist')
    ax.set_ylabel('Velocity')

    plt.show()
    '''
    boxplot = adjusted_results.boxplot()
    boxplot.set_xlabel('Biker')
    boxplot.set_ylabel('Velocity')
    boxplot.set_title(plot_type)
    plt.show()
    '''


def fun_distro_diagram(summary_dict, plot_type='Fun_Distribution_Motorcyclist'):
    """
    Plots the fun distribution of the motorcyclists over time/steps
    :param summary_dict:
    :param plot_type:
    :return:
    """
    adjusted_results = extractor_summary_dict(summary_dict, plot_type=plot_type)

    # if dataframe is empty skip plot
    if adjusted_results.empty:
        print(f'empty df for {plot_type}')
        return

    ax = adjusted_results.plot(title=plot_type)
    ax.set_xlabel('Time')
    ax.set_ylabel('Fun')
    ax.set_title(plot_type)
    plt.show()


def extractor_summary_dict(summary_dict, plot_type):
    """
    Extracts the data from the summary dict and returns a dict with the adjusted data for different plots
    :param summary_dict:
    :param plot_type:
    :return:
    """
    data = None

    # Creates a DF from summary_dict for a time distance diagram for Motorcyclist only
    if plot_type == 'Time_Distance_Diagram_Motorcyclist':
        motorcyclist_only = {}

        for key in summary_dict:
            if summary_dict[key]['vehicle_type'] == 'Motorcycle':
                motorcyclist_only[key] = summary_dict[key]['travel_list']

        # convert dict into dataframe. Columns are the travel distance from each motorcyclist
        data = pd.DataFrame.from_dict(motorcyclist_only)

        # rename columns to Biker_vehicle index
        for col in data.columns:
            name = 'Biker ' + str(col)
            data.rename(columns={col: name}, inplace=True)

        # cumulate the data for each biker
        for col in data.columns:
            data[col] = data[col].cumsum()

    # Creates a DF from summary_dict for a time distance diagram for Cars only
    elif plot_type == 'Time_Distance_Diagram_Car':
        car_only = {}

        for key in summary_dict:
            if summary_dict[key]['vehicle_type'] == 'Car':
                car_only[key] = summary_dict[key]['travel_list']

        # convert dict into dataframe. Columns are the travel distance from each car
        data = pd.DataFrame.from_dict(car_only)

        # rename columns to Car_vehicle index
        for col in data.columns:
            name = 'Car ' + str(col)
            data.rename(columns={col: name}, inplace=True)

        # cumulate the data for each car
        for col in data.columns:
            data[col] = data[col].cumsum()

    # Creates a DF from summary_dict for a velocity distribution diagram for Motorcyclist only
    elif plot_type == 'Velocity_Distribution_Motorcyclist':
        motorcyclist_only = {}

        for key in summary_dict:
            if summary_dict[key]['vehicle_type'] == 'Motorcycle':
                motorcyclist_only[key] = summary_dict[key]['travel_list']

        # convert dict into dataframe. Columns are the travel distance from each motorcyclist
        data = pd.DataFrame.from_dict(motorcyclist_only)

        # rename columns to Biker_vehicle index
        for col in data.columns:
            name = 'Biker ' + str(col)
            data.rename(columns={col: name}, inplace=True)

    # Todo check fun curve
    # Creates a DF from summary_dict for a fun distribution diagram for Motorcyclist only
    elif plot_type == 'Fun_Distribution_Motorcyclist':
        fun_motorcyclist_only = {}

        for key in summary_dict:
            if summary_dict[key]['vehicle_type'] == 'Motorcycle':
                fun_motorcyclist_only[key] = summary_dict[key]['fun_list']

        # convert dict into dataframe. Columns are the fun for each motorcyclist
        data = pd.DataFrame.from_dict(fun_motorcyclist_only)

        # rename columns to Biker_vehicle index
        for col in data.columns:
            name = 'Biker ' + str(col)
            data.rename(columns={col: name}, inplace=True)

    else:
        raise ValueError('Plot type not supported')

    return data
