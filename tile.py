class Tile:
    def __init__(self, index, lane, vehicle=None, curvature=0):
        self.index = index
        self.lane = lane
        self.vehicle = vehicle
        self.curvature = curvature

    def set_vehicle(self, vehicle):
        self.vehicle = vehicle

    def get_icon(self):
        if self.vehicle is None:
            if self.get_index() % 10 == 0:
                return '  |  '
            else:
                return '  .  '

        else:
            return self.vehicle.get_icon()

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
