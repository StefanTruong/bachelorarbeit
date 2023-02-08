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


def fun_distro_diagram_with_errorbar(sum_fun_data, plot_type='Fun_Distribution_with_errorbar_Motorcyclist'):
    """
    Plots the fun distribution of the motorcyclists over time/steps with errorbar
    :param summary_dict:
    :param plot_type:
    :return:
    """
    mean_fun_dict, z_score_fun_dict = extractor_summary_dict(sum_fun_data, plot_type=plot_type)

    # time-steps for the x-values as list for x-axis plotting
    time_steps = []
    length = 0
    for biker, mean_fun in mean_fun_dict.items():
        if len(mean_fun) > length:
            length = len(mean_fun)
            time_steps = list(range(length))

    for biker, mean_fun in mean_fun_dict.items():
        plt.errorbar(time_steps, mean_fun, xerr=0, yerr=np.array(z_score_fun_dict[biker]), elinewidth=0.15, label=biker)

    # calculate std for all z scores for all bikers and plot them
    all_z_scores = []
    all_mean_fun = []
    for biker, z_score_fun in z_score_fun_dict.items():
        all_z_scores.append(z_score_fun)

    for biker, mean_fun in mean_fun_dict.items():
        all_mean_fun.append(mean_fun)

    print('mean for all means', np.mean(all_mean_fun))
    print('mean for all z_scores', np.mean(all_z_scores))

    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Fun')
    plt.title(plot_type)
    plt.show()


def time_distance_diagram_with_errorbar(sum_time_distance_data,
                                        plot_type='Time_Distance_Diagram__with_errorbar_Motorcyclist'):
    mean_dist_dict, std_dist_dict = extractor_summary_dict(sum_time_distance_data, plot_type=plot_type)

    # time-steps for the x-values as list for x-axis plotting
    time_steps = []
    length = 0
    for biker, mean_distance in mean_dist_dict.items():
        if len(mean_distance) > length:
            length = len(mean_distance)
            time_steps = list(range(length))

    for biker, mean_fun in mean_dist_dict.items():
        plt.errorbar(time_steps, mean_fun, xerr=0, yerr=np.array(std_dist_dict[biker]), elinewidth=0.15, label=biker)

    # calculate std for all std for all bikers and plot them
    all_mean_fun = []
    all_std_scores = []
    for biker, z_score_fun in std_dist_dict.items():
        all_std_scores.append(z_score_fun)

    for biker, mean_fun in mean_dist_dict.items():
        all_mean_fun.append(mean_fun)

    print('mean for all means', np.mean(all_mean_fun))
    print('mean for all std_errors', np.mean(all_std_scores))

    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Distance')
    plt.title(plot_type)
    plt.show()


def extractor_summary_dict(my_dict, plot_type):
    """
    Extracts the data from the summary dict and returns a dict with the adjusted data for different plots
    :param my_dict: can be the actual summary dict or some adjusted one!!!
    :param plot_type:
    :return:
    """
    data = None

    # Creates a DF from summary_dict for a time distance diagram for Motorcyclist only
    if plot_type == 'Time_Distance_Diagram_Motorcyclist':
        motorcyclist_only = {}

        for key in my_dict:
            if my_dict[key]['vehicle_type'] == 'Motorcycle':
                motorcyclist_only[key] = my_dict[key]['travel_list']

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

        for key in my_dict:
            if my_dict[key]['vehicle_type'] == 'Car':
                car_only[key] = my_dict[key]['travel_list']

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

        for key in my_dict:
            if my_dict[key]['vehicle_type'] == 'Motorcycle':
                motorcyclist_only[key] = my_dict[key]['travel_list']

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

        for key in my_dict:
            if my_dict[key]['vehicle_type'] == 'Motorcycle':
                fun_motorcyclist_only[key] = my_dict[key]['fun_list']

        # convert dict into dataframe. Columns are the fun for each motorcyclist
        data = pd.DataFrame.from_dict(fun_motorcyclist_only)

        # rename columns to Biker_vehicle index
        for col in data.columns:
            name = 'Biker ' + str(col)
            data.rename(columns={col: name}, inplace=True)

    elif plot_type == 'Fun_Distribution_with_errorbar_Motorcyclist':
        mean_fun_motorcyclist_only = {}
        z_score_fun_motorcyclist_only = {}

        # calculate average and z scores for each biker to each time step
        for biker, values in my_dict.items():
            mean_for_all_time_steps = []
            z_score_for_all_time_steps = []

            for fun_list_at_time_step in values:
                mean = np.mean(fun_list_at_time_step)
                std = np.std(fun_list_at_time_step)
                z_score_at_time_step = []
                for fun_value in fun_list_at_time_step:
                    z_score = (fun_value - mean) / std
                    z_score_at_time_step.append(z_score)

                mean_for_all_time_steps.append(mean)
                z_score_for_all_time_steps.append(z_score_at_time_step)

            mean_fun_motorcyclist_only[biker] = mean_for_all_time_steps
            z_score_fun_motorcyclist_only[biker] = mean_for_all_time_steps

        data = [mean_fun_motorcyclist_only, z_score_fun_motorcyclist_only]

    elif plot_type == 'Time_Distance_Diagram__with_errorbar_Motorcyclist':
        mean_dist_motorcyclist_only = {}
        std_dist_motorcyclist_only = {}

        # calculate average and std for each biker to each time step
        for biker, values in my_dict.items():
            mean_for_all_time_steps = []
            std_for_all_time_steps = []

            for dist_list_at_time_step in values:
                mean = np.mean(dist_list_at_time_step)
                std = np.std(dist_list_at_time_step)

                mean_for_all_time_steps.append(mean)
                std_for_all_time_steps.append(std)

            mean_dist_motorcyclist_only[biker] = mean_for_all_time_steps
            std_dist_motorcyclist_only[biker] = std_for_all_time_steps

        data = [mean_dist_motorcyclist_only, std_dist_motorcyclist_only]

    else:
        raise ValueError('Plot type not supported')

    return data
