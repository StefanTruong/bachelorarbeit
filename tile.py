class Tile:
    def __init__(self, index, lane, vehicle=None, curvature=0, beauty=0):
        self.index = index
        self.lane = lane
        self.vehicle = vehicle
        self.curvature = curvature
        self.beauty = beauty

    def set_vehicle(self, vehicle):
        self.vehicle = vehicle

    def set_curvature(self, curvature):
        self.curvature = curvature

    def get_icon(self):
        """
        returns the icon of the vehicle on the tile
        :return:
        """
        if self.vehicle is None:
            if self.get_index() % 10 == 0:
                return '  |  '
            else:
                return '  .  '

        else:
            return self.vehicle.get_icon()

    def get_icon_curve(self):
        """
        returns the curvature of the tile as a string
        :return:
        """
        icon = str(self.curvature)
        if len(icon) == 1:
            return '  ' + icon + '  '
        elif len(icon) == 2:
            return '  ' + icon + ' '

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
