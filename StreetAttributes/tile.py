class Tile:
    def __init__(self, index, lane, vehicle=None, curvature=0, beauty=0):
        """
        the tile on which the vehicles are moving
        :param index: index of the section the tile is in
        :param lane: on which lane the tile is
        :param vehicle: the vehicle on the tile
        :param curvature: curve of the tile
        :param beauty: the beauty of the tile (optional)
        :param speed_limit: the speed limit of the tile depending on curvature. If no data available use max values
        """
        self.index = index
        self.lane = lane
        self.vehicle = vehicle
        self.curvature = curvature
        self.beauty = beauty
        self.speed_limit = 100

    def set_vehicle(self, vehicle):
        self.vehicle = vehicle

    def set_curvature(self, curvature):
        self.curvature = curvature

    def set_beauty(self, beauty):
        self.beauty = beauty

    def set_speed_limit(self, speed_limit):
        self.speed_limit = speed_limit

    def get_icon(self):
        """
        returns the icon of the vehicle on the tile
        :return:
        """
        if self.vehicle is None:
            if self.get_index() % 10 == 0:
                return '|    '
            else:
                return '.    '

        else:
            return self.vehicle.get_icon()

    def get_icon_curve(self):
        """
        returns the curvature of the tile as a string. Since Curvature range [0,9999]
        :return:
        """
        # curvature symbols depends on config.py
        symbol_to_curvature = {
            'o': range(0, 500),
            '~': range(500, 1000),
            '~~': range(1000, 1500),
            '~~~': range(1500, 2000),
            '~~~~': range(2000, 5000),
            '~~~~~': range(5000, 20000)
        }

        icon = 'error'
        for key in symbol_to_curvature:
            if self.get_curvature() in symbol_to_curvature[key]:
                icon = key

        # icon = str(self.curvature)
        if len(icon) == 1:
            return '' + icon + '    '
        elif len(icon) == 2:
            return '' + icon + '   '
        elif len(icon) == 3:
            return '' + icon + '  '
        elif len(icon) == 4:
            return '' + icon + ' '
        elif len(icon) == 5:
            return '' + icon + ''

    def get_icon_speed_limit(self):
        """
        returns the speed limit for visualization
        :return:
        """
        icon = str(self.speed_limit)
        if len(icon) == 1:
            return '' + icon + '    '
        elif len(icon) == 2:
            return '' + icon + '   '
        elif len(icon) == 3:
            return '' + icon + '  '
        elif len(icon) == 4:
            return '' + icon + ' '

    def get_icon_granular(self):
        """
        returns the icon of the vehicle on the tile for a 2D Plot.
        :return: integer 1 if there is a vehicle. integer 0 if there is None
        """
        if self.vehicle is None:
            return 0
        else:
            return 1

    def get_index(self):
        return self.index

    def get_lane(self):
        return self.lane

    def get_vehicle(self):
        return self.vehicle

    def get_curvature(self):
        return self.curvature

    def get_speed_limit(self):
        return self.speed_limit

    def get_beauty(self):
        return self.beauty

