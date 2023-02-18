import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 20
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
    :param sum_fun_data:
    :param plot_type:
    :return:
    """
    mean_fun_dict, std_fun_dict = extractor_summary_dict(sum_fun_data, plot_type=plot_type)
    sum_fun = extractor_summary_dict(sum_fun_data, plot_type='sum_fun')

    # time-steps for the x-values as list for x-axis plotting
    time_steps = []
    length = 0
    for biker, mean_fun in mean_fun_dict.items():
        if len(mean_fun) > length:
            length = len(mean_fun)
            time_steps = list(range(length))

    for biker, mean_fun in mean_fun_dict.items():
        plt.errorbar(time_steps, mean_fun, xerr=0, yerr=np.array(std_fun_dict[biker]), elinewidth=0.08, label=biker)

    # calculate std for all z scores for all bikers and plot them
    all_z_scores = []
    all_mean_fun = []
    for biker, std_score_fun in std_fun_dict.items():
        all_z_scores.append(std_score_fun)

    for biker, mean_fun in mean_fun_dict.items():
        all_mean_fun.append(mean_fun)

    print('---------------------------------------------------------------------')
    print('sum of all fun (has to be divided by #steps and #loops again)', sum_fun)
    print('mean for all means', np.mean(all_mean_fun))
    print('mean for all std', np.mean(all_z_scores))
    print('---------------------------------------------------------------------')

    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Fun')
    plt.title(plot_type)
    plt.show()


def fun_distro_histogram(sum_fun_data, time_steps, plot_type='Fun_Histogram_Motorcyclist'):
    """
    Plots the fun histogram of the motorcyclists
    :param time_steps:
    :param sum_fun_data:
    :param plot_type:
    :return:
    """
    # Hint uses same summary logic as fun_distro_diagram_with_errorbar. Thus use plot_type is overwritten
    mean_fun_dict, std_fun_dict = extractor_summary_dict(sum_fun_data, plot_type='Fun_Distribution_with_errorbar_Motorcyclist')
    sum_fun = extractor_summary_dict(sum_fun_data, plot_type='sum_fun')

    # transform dict to dataframe into an average for all time steps
    df = pd.DataFrame.from_dict(mean_fun_dict, orient='index')

    # summarize columns and use summary as new column. Sum is the last row. Drop all other rows except the last one
    df['sum'] = df.sum(axis=1)/time_steps
    df = df.transpose()
    n = len(df)
    df.drop(df.head(n-1).index, inplace=True)
    print(df)
    print(df.transpose())
    # plot histogram and rotate x-axis labels

    ax = df.transpose().plot(kind='bar', title=plot_type, rot=0)
    ax.set_xlabel('Motorcyclist')
    ax.set_ylabel('Fun')
    plt.show()

def time_distance_diagram_with_errorbar(sum_time_distance_data,
                                        plot_type='Time_Distance_Diagram_with_errorbar_Motorcyclist'):
    """
    plots a time-distance diagram with errorbars for multiple runs
    :param sum_time_distance_data:
    :param plot_type:
    :return:
    """
    mean_dist_dict, std_dist_dict = extractor_summary_dict(sum_time_distance_data, plot_type=plot_type)
    sum_dist = extractor_summary_dict(sum_time_distance_data, plot_type='sum_dist')

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
    all_mean_distance = []
    all_std_scores = []
    for biker, std_fun in std_dist_dict.items():
        all_std_scores.append(std_fun)

    for biker, mean_fun in mean_dist_dict.items():
        all_mean_distance.append(mean_fun)

    print('---------------------------------------------------------------------')
    print('sum of all distance (has to be divided by #steps and #loops again)', sum_dist)
    print('mean for all means distance (Times 2X to be at the end)', np.mean(all_mean_distance))
    print('mean for all std_errors distance', np.mean(all_std_scores))
    print('---------------------------------------------------------------------')

    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Distance')
    plt.title(plot_type)
    plt.show()


def velocity_distribution_histogram(sum_velocity_data,
                                    plot_type='Velocity_Distribution_Diagram_with_errorbar_Motorcyclist'):
    """
    plots the velocity distribution diagram with errorbars for multiple runs
    :param sum_velocity_data: a dict of velocities of the motorcyclists for all runs
    :param plot_type:
    :return:
    """
    velocity_dict_to_df = extractor_summary_dict(sum_velocity_data, plot_type=plot_type)

    # if dataframe is empty skip plot
    if velocity_dict_to_df.empty:
        print(f'empty df for {plot_type}')
        return

    # cmap = cm.ScalarMappable(cmap='rainbow')
    ax = velocity_dict_to_df.plot(kind='box', title=plot_type)
    ax.set_xlabel('Motorcyclist')
    ax.set_ylabel('Velocity')

    plt.show()


def lane_diagram(left_lane_data, right_lane_data, plot_type='Percentage_being_on_the_right_lane'):
    """
    plots the percentage a motorcyclist was on th right lane
    :param left_lane_data:
    :param right_lane_data:
    :param plot_type:
    :return:
    """
    # how long a biker was on the left lane or right lane respectively
    sum_on_left_lane = {}
    sum_on_right_lane = {}

    for biker, on_left_lane in left_lane_data.items():
        increment = sum(on_left_lane)
        sum_on_left_lane[biker] = increment

    for biker, on_right_lane in right_lane_data.items():
        increment = sum(on_right_lane)
        sum_on_right_lane[biker] = increment

    # calculate the percentage of time a biker was on the right lane
    percentage_on_right_lane = {}
    for biker, on_left_lane in sum_on_left_lane.items():
        percentage_on_right_lane[biker] = sum_on_right_lane[biker] / (sum_on_right_lane[biker] + on_left_lane)

    # plot the percentage of time a biker was on the right lane
    plt.bar(percentage_on_right_lane.keys(), percentage_on_right_lane.values(), width=0.2)
    plt.xlabel('Motorcyclist')
    plt.ylabel('Share being on the right Lane [%]')
    plt.title(plot_type)
    plt.show()


def role_diagram(sum_role_data, plot_type='Role_Distribution_Histogram'):
    """
    plots the role diagram histogram for all motorcyclists.
    First row in sum_role_data is the sum how often a biker was the sweeper
    Second row in sum_role_data is the sum how often a biker was the inbetween
    Third row in sum_role_data is the sum how often a biker was the leader
    column represents the biker
    :param sum_role_data:
    :param plot_type:
    :return:
    """
    sum_role_percentage = extractor_summary_dict(sum_role_data, plot_type=plot_type)

    # rename the index of the dataframe
    sum_role_percentage.index = ['Sweeper', 'Inbetween', 'Leader', 'Lost']

    ax = sum_role_percentage.plot(kind='bar', title=plot_type)
    # rotate the x-axis labels
    ax.set_xticklabels(sum_role_percentage.index, rotation=0)
    ax.set_xlabel('Roles')
    ax.set_ylabel('Share being in a Role [%]')
    plt.title(plot_type)

    plt.show()


def distance_to_partner_diagram(sum_behind_distance_to_partner_data, sum_ahead_distance_to_partner_data,
                                plot_type='Distance_to_partner_Distribution'):
    """
    Plots the distance to partner distribution over time for all motorcyclists with error bars.
    None values are converted to 0
    sum_behind_distance_to_partner_data = {'Biker4': [[times of runs], [], time_steps], ..., 'Biker0': [[time of runs], [], time_steps]}
    :param sum_behind_distance_to_partner_data:
    :param sum_ahead_distance_to_partner_data:
    :param plot_type:
    :return:
    """
    # collects all the distances of each run together in a dict with list of list as values
    # {'Biker 4': [[0, 0, None, None], [values of runs behind and ahead], [0, 0, None, None]], 'Biker 3': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], ...}
    distance_summarized_all_bikers = {}
    for biker, values in sum_behind_distance_to_partner_data.items():
        distance_summarized_each_biker = {biker: None}
        distance_over_time = []
        time_step = 0
        for element in values:
            distance_at_time_step = sum_behind_distance_to_partner_data[biker][time_step]
            distance_at_time_step = [*distance_at_time_step, *sum_ahead_distance_to_partner_data[biker][time_step]]
            distance_over_time.append(distance_at_time_step)
            distance_summarized_each_biker[biker] = distance_over_time
            time_step += 1

        distance_summarized_all_bikers[biker] = distance_summarized_each_biker[biker]

    # calculate the mean and std of the distance to partner for each biker
    distance_means_for_all_bikers = {}
    distance_std_for_all_bikers = {}
    for biker, values_at_time_step in distance_summarized_all_bikers.items():
        distance_means_for_each_biker = []
        distance_std_for_each_biker = []
        for time_step in values_at_time_step:
            mean = np.mean(time_step)
            std = np.std(time_step)
            distance_means_for_each_biker.append(mean)
            distance_std_for_each_biker.append(std)
        distance_means_for_all_bikers[biker] = distance_means_for_each_biker
        distance_std_for_all_bikers[biker] = distance_std_for_each_biker

    # print(distance_summarized_all_bikers)
    # print(distance_means_for_all_bikers)

    # plot the distance with error bars to partner for each biker
    for biker, values in distance_means_for_all_bikers.items():
        plt.errorbar(range(len(values)), values, yerr=distance_std_for_all_bikers[biker], elinewidth=0.25, label=biker)

    plt.xlabel('Time Step')
    plt.ylabel('Distance to Partner [m]')
    plt.title(plot_type)
    plt.legend()
    plt.show()
    plt.clf()

    # summarize mean values across all bikers
    aggregated_mean_distance = []
    aggregated_std_distance = []
    num_time_steps = len(distance_means_for_all_bikers['Biker 0'])
    num_bikers = len(distance_means_for_all_bikers.keys())
    for time in range(num_time_steps):
        aggregated_means = []
        aggregated_std = []
        for biker in distance_means_for_all_bikers.keys():
            aggregated_means.append(distance_means_for_all_bikers[biker][time])
            aggregated_std.append(distance_std_for_all_bikers[biker][time])
        aggregated_mean_distance.append(np.sum(aggregated_means) / num_bikers)
        aggregated_std_distance.append(np.sum(aggregated_std) / num_bikers)

    # calculate the aggregated sum mean distance
    mean_mean_distance = np.mean(aggregated_mean_distance)
    mean_std_distance = np.mean(aggregated_std_distance)

    print('sum_mean_distance', mean_mean_distance)
    print('sum_std_distance', mean_std_distance)

    # plot the aggregated mean distance with error bars
    plt.errorbar(range(len(aggregated_mean_distance)), aggregated_mean_distance, yerr=aggregated_std_distance,
                 elinewidth=0.25)
    plt.xlabel('Time')
    plt.ylabel('Average Distance to Partner [m]')
    plt.title(plot_type)
    plt.show()


def extractor_summary_dict(my_dataobj, plot_type):
    """
    Extracts the data from the summary dict and returns a dict with the adjusted data for different plots
    :param my_dataobj: can be the actual summary dict or a dataframe!!!
    :param plot_type:
    :return:
    """
    data = None

    # Creates a DF from summary_dict for a time distance diagram for Motorcyclist only
    if plot_type == 'Time_Distance_Diagram_Motorcyclist':
        motorcyclist_only = {}

        for key in my_dataobj:
            if my_dataobj[key]['vehicle_type'] == 'Motorcycle':
                motorcyclist_only[key] = my_dataobj[key]['travel_list']

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

        for key in my_dataobj:
            if my_dataobj[key]['vehicle_type'] == 'Car':
                car_only[key] = my_dataobj[key]['travel_list']

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

        for key in my_dataobj:
            if my_dataobj[key]['vehicle_type'] == 'Motorcycle':
                motorcyclist_only[key] = my_dataobj[key]['travel_list']

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

        for key in my_dataobj:
            if my_dataobj[key]['vehicle_type'] == 'Motorcycle':
                fun_motorcyclist_only[key] = my_dataobj[key]['fun_list']

        # convert dict into dataframe. Columns are the fun for each motorcyclist
        data = pd.DataFrame.from_dict(fun_motorcyclist_only)

        # rename columns to Biker_vehicle index
        for col in data.columns:
            name = 'Biker ' + str(col)
            data.rename(columns={col: name}, inplace=True)

    elif plot_type == 'Fun_Distribution_with_errorbar_Motorcyclist':
        mean_fun_motorcyclist_only = {}
        std_fun_motorcyclist_only = {}

        # calculate average and z scores for each biker to each time step
        for biker, values in my_dataobj.items():
            mean_for_all_time_steps = []
            std_for_all_time_steps = []

            for fun_list_at_time_step in values:
                mean = np.mean(fun_list_at_time_step)
                std = np.std(fun_list_at_time_step)

                mean_for_all_time_steps.append(mean)
                std_for_all_time_steps.append(std)

            mean_fun_motorcyclist_only[biker] = mean_for_all_time_steps
            std_fun_motorcyclist_only[biker] = std_for_all_time_steps

        data = [mean_fun_motorcyclist_only, std_fun_motorcyclist_only]

    elif plot_type == 'sum_fun':
        sum_fun = 0
        for biker, values in my_dataobj.items():
            for time_data in values:
                sum_fun += np.sum(time_data)

        data = sum_fun

    elif plot_type == 'Time_Distance_Diagram_with_errorbar_Motorcyclist':
        mean_dist_motorcyclist_only = {}
        std_dist_motorcyclist_only = {}

        # calculate average and std for each biker to each time step
        for biker, values in my_dataobj.items():
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

    elif plot_type == 'sum_dist':
        sum_dist = 0
        for biker, values in my_dataobj.items():
            for time_data in values:
                sum_dist += np.sum(time_data)

        data = sum_dist

    elif plot_type == 'Velocity_Distribution_Diagram_with_errorbar_Motorcyclist':
        # number of time steps
        time_steps = len(my_dataobj['Biker 0'][0])

        avg_dict = {}
        for biker, num_runs in my_dataobj.items():
            avg_dict[biker] = []
            velo_at_time_i = []
            for i in range(time_steps):
                for run in num_runs:
                    velo_at_time_i.append(run[i])
                avg_dict[biker].append(np.mean(velo_at_time_i))
                velo_at_time_i = []

        # converts dict to dataframe
        converted_dict_to_df = pd.DataFrame.from_dict(avg_dict)
        data = converted_dict_to_df

    elif plot_type == 'Role_Distribution_Histogram':
        # calculates percentage of each role in a dataframe
        for column in my_dataobj:
            my_dataobj[column] = my_dataobj[column] / sum(my_dataobj[column]) * 100

        data = my_dataobj

    else:
        raise ValueError('Plot type not supported')

    return data
