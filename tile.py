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
            # ToDo remove icon should be just '  .  '. This is for debugging only
            if self.get_index() % 10 == 0:
                return '  |  '
            else:
                return '  .  '

        else:
            return self.vehicle.get_icon()

    def get_index(self):
        return self.index

    def get_lane(self):
        return self.lane

    def get_vehicle(self):
        return self.vehicle

    def get_curvature(self):
        return self.curvature
