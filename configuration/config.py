import numpy as np

class ConfigPreference:
    def __init__(self, configuration=None):
        if configuration is None or configuration == 'default':




if __name__ == '__main__':
    config = ConfigPreference('default')
    print(vars(config))
