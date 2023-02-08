import json


class AnalyseResult:

    def __init__(self):
        self.result = None
        self.fun_results = None

    def add_dataframes(self, df1, save='fun_data'):
        """
        add two dataframes, where elements are lists
        :return:
        """
        if save == 'fun_data':
            # convert dataframe to a dict with list element
            dict_with_list_elements = {}
            for key, series in df1.iteritems():
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

    def get_fun_data(self):
        return self.fun_results

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
