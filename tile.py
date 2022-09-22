class Tile:
    def __init__(self, index, lane, vehicle=None, curvature=0):
        self.index = index
        self.lane = lane
        self.vehicle = vehicle
        self.curvature = curvature

    def get_icon(self):
        if self.vehicle is None:
            return '.'
        else:
            return self.vehicle.icon
