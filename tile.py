class Tile:
    def __init__(self, index, lane, vehicle=None, curvature=0, x=0, y=0):
        self.index = index
        self.lane = lane
        self.vehicle = vehicle
        self.curvature = curvature
        self.x = x
        self.y = y