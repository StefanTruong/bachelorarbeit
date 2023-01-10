import json


class AnalyseResult:

    def __init__(self):
        self.result = None

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
