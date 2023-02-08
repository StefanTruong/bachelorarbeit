import json


class AnalyseResult:

    def __init__(self):
        self.result = None
        self.fun_results = None
        self.time_distance_results = None
        self.velocity_results = None
        self.sum_left_lane_results = None
        self.sum_right_lane_results = None
        self.role_results = None

    def add_dataframes(self, dataframe, temp_save):
        """
        add two dataframes, where elements are lists
        :return:
        {'Biker 4': [[number of loops],
                      number of time
                        ],
        ...
        }
        """
        if temp_save == 'fun_data':
            # convert dataframe to a dict with list element for each time
            dict_with_list_elements = {}
            for key, series in dataframe.iteritems():
                dict_with_list_elements[key] = []
                series = series.tolist()
                for element in series:
                    dict_with_list_elements[key].append([element])

            if self.fun_results is None:
                self.fun_results = dict_with_list_elements
            else:
                for key, value in dict_with_list_elements.items():
                    for i in range(0, len(value)):
                        self.fun_results[key][i] += value[i]

        elif temp_save == 'time_distance_data':
            # convert dataframe to a dict with list element for each time
            dict_with_list_elements = {}
            for key, series in dataframe.iteritems():
                dict_with_list_elements[key] = []
                series = series.tolist()
                for element in series:
                    dict_with_list_elements[key].append([element])

            if self.time_distance_results is None:
                self.time_distance_results = dict_with_list_elements
            else:
                for key, value in dict_with_list_elements.items():
                    for i in range(0, len(value)):
                        self.time_distance_results[key][i] += value[i]

        elif temp_save == 'velocity_distribution_data':
            # convert dataframe to a dict collecting all velocities over time
            if self.velocity_results is None:
                self.velocity_results = {}
                for col in dataframe.columns:
                    self.velocity_results[col] = dataframe[col]
            else:
                for col in dataframe.columns:
                    self.velocity_results[col] = [*self.velocity_results[col], *dataframe[col]]

        elif temp_save == 'left_lane_data' or temp_save == 'right_lane_data':
            # convert dataframe to a dict collecting all velocities over time

            if temp_save == 'left_lane_data':
                if self.sum_left_lane_results is None:
                    self.sum_left_lane_results = {}
                    for col in dataframe.columns:
                        self.sum_left_lane_results[col] = dataframe[col]
                else:
                    for col in dataframe.columns:
                        self.sum_left_lane_results[col] = [*self.sum_left_lane_results[col], *dataframe[col]]

            else:
                if self.sum_right_lane_results is None:
                    self.sum_right_lane_results = {}
                    for col in dataframe.columns:
                        self.sum_right_lane_results[col] = dataframe[col]
                else:
                    for col in dataframe.columns:
                        self.sum_right_lane_results[col] = [*self.sum_right_lane_results[col], *dataframe[col]]

        elif temp_save == 'role_data':
            # Biker 4 | ... | Biker 0
            # 0     0 | ... | 3         first row is the role sweeper
            # 1     0 | ... | 0         second row is the role inbetween
            # 2     3 | ... | 0         third row is the role leader
            if self.role_results is None:
                self.role_results = dataframe
            else:
                self.role_results += dataframe

        else:
            raise Exception('unknown temp_save modus')

    def get_aggregated_fun_data(self):
        return self.fun_results

    def get_aggregated_time_distance_data(self):
        return self.time_distance_results

    def get_aggregated_velocity_data(self):
        return self.velocity_results

    def get_aggregated_left_lane_data(self):
        return self.sum_left_lane_results

    def get_aggregated_right_lane_data(self):
        return self.sum_right_lane_results

    def get_aggregated_role_data(self):
        return self.role_results

    def load_result(self, filename=None):
        """
        loads the result dict
        :param filename:
        :return:
        """
        if filename is None:
            fp = open('./results.json')
            result = json.load(fp)
            self.result = result
        else:
            pass


def main():
    # load result dictionary
    analyzer = AnalyseResult()
    analyzer.load_result()
    print()


if __name__ == '__main__':
    main()
