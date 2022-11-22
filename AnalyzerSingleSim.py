from MyTrafficSimulation import *
import copy
import numpy as np


class AnalyzerSingleSim:
    """
    analyzes changes in the movement of the vehicles and summarize them
    """
    def __init__(self, simulation: TrafficSimulation):
        self.simulation = simulation
        self.step = 0
        self.flow = 0
        self.old_vehicle_list = copy.deepcopy(simulation.get_vehicle_list())
        self.new_vehicle_list = None
        self.vehicle_summary_dict = None

        self.init_vehicle_summary_dict()

    def update(self):
        """
        updates step and flow as well as vehicle_summary dict. Has to be called each step
        :return:
        """
        self.incr_step()
        self.update_flow_all_lanes()
        self.update_new_vehicle_list()
        self.update_vehicle_summary_dict()
        self.update_old_vehicle_list()

    def init_vehicle_summary_dict(self):
        """
        initializes the vehicle summary data in preparation for analysis from old_vehicle_list
        :return:
        """
        summary_dict = {}
        for vehicle in self.old_vehicle_list:
            summary_dict[vehicle.get_id()] = {
                'new_pos': vehicle.get_tile().get_index(),  # the current tile index
                'old_pos': vehicle.get_tile().get_index(),  # old tile index
                'sum_traveling_dist': 0,  # sum of travel distance
                'new_speed': vehicle.get_speed(),  # current speed
                'old_speed': vehicle.get_speed(),  # the speed before
                'avg_speed': 0,  # avg speed in current step
                'new_lane': vehicle.get_tile().get_lane(),
                'old_lane': vehicle.get_tile().get_lane(),
                'change_lane': False,  # has it switched lane currently
                'sum_change_lane': 0,  # sum of switched lanes

                # ToDo add changes to update_vehicle_summary_dict
                'sum_ping_pong_lane_changes': 0,    # sum of ping pong lane changes
                'behind_dist_partner': 0,           # motorcyclist distance of behind partner
                'sum_behind_dist_partner': 0,       # sum of the distance of the behind partner
                'avg_behind_dist_partner': 0,       # avg sum of the dist of the behind partner
                'std_behind_dist_partner': 0,       # std of the dist of the behind partner
                'ahead_dist_partner': 0,            # motorcyclist distance of ahead partner
                'sum_ahead_dist_partner': 0,        # sum of the distance of the ahead partner
                'avg_ahead_dist_partner': 0,        # avg sum of the dist of the ahead partner
                'std_ahead_dist_partner': 0,        # std of the dist of the behind partner
                'sum_on_left_lane': 0,              # how long the motorcyclist was on the left lane
                'sum_on_right_lane': 0,             # how long the motorcyclist was on the right lane
                'incr_fun': 0,                      # motorcyclist fun in this step
                'sum_fun': 0                        # motorcyclist overall fun
            }
        self.vehicle_summary_dict = summary_dict

    def update_vehicle_summary_dict(self):
        """
        updates vehicle_summary_dict with new data from new_vehicle_list
        :return:
        """
        for vehicle in self.new_vehicle_list:
            i = vehicle.get_id()

            # the former new position is now the old position. The new one is the current position
            self.vehicle_summary_dict[i]['old_pos'] = self.vehicle_summary_dict[i]['new_pos']
            self.vehicle_summary_dict[i]['new_pos'] = vehicle.get_tile().get_index()

            # the vehicle has traveled so far as its current saved speed
            self.vehicle_summary_dict[i]['sum_traveling_dist'] += vehicle.get_speed()

            # the former new speed is now the old speed. The new one is the current speed
            self.vehicle_summary_dict[i]['old_speed'] = self.vehicle_summary_dict[i]['new_speed']
            self.vehicle_summary_dict[i]['new_speed'] = vehicle.get_speed()

            # calc new average speed.
            self.vehicle_summary_dict[i]['avg_speed'] = self.vehicle_summary_dict[i]['sum_traveling_dist'] / self.step

            # if a lane change occurs update it. the former new lane is the old lane
            if self.vehicle_summary_dict[i]['new_lane'] != vehicle.get_tile().get_lane():
                self.vehicle_summary_dict[i]['change_lane'] = True
                self.vehicle_summary_dict[i]['sum_change_lane'] += 1
                self.vehicle_summary_dict[i]['old_lane'] = self.vehicle_summary_dict[i]['new_lane']
                self.vehicle_summary_dict[i]['new_lane'] = vehicle.get_tile().get_lane()
            else:
                self.vehicle_summary_dict[i]['change_lane'] = False

    def incr_step(self):
        """
        increments the step
        :return:
        """
        self.step += 1

    def update_flow_all_lanes(self):
        """
        measures densities on a fixed site. Here at tile index = 0 averaged over a time period T. See Nasch p.2223
        max velocity has car with 12 tiles
        :return:
        """
        max_velocity = 10
        for lane in range(0, self.simulation.num_lanes + 1):
            for pos in range(0, max_velocity + 1):
                if self.simulation.get_tiles()[pos][lane].get_vehicle() is not None:
                    if self.simulation.get_tiles()[pos][lane].get_vehicle().get_speed() > pos:
                        self.flow += 1

    def update_new_vehicle_list(self):
        """
        reads the actual vehicle_list from MyTrafficSimulation
        :return:
        """
        self.new_vehicle_list = copy.deepcopy(self.simulation.get_vehicle_list())

    def update_old_vehicle_list(self):
        """
        sets the last new vehicle_list to the old_vehicle list
        :return:
        """
        self.old_vehicle_list = self.new_vehicle_list

    def get_traffic_flow_all_lanes(self):
        """
        calculates the flow rate for a single run. Has to be divided by number of lanes
        :return:
        """
        return (self.flow / self.step) / (self.simulation.get_lanes() + 1)

    def get_simulation(self):
        return self.simulation


class SaveResults:
    def __init__(self):
        self.density_list = []
        self.singleFlows = []

    def collect_flow_density(self, analyzer: AnalyzerSingleSim):
        """
        collects data each single time a simulation with a density is finished.
        Use it when a loop with different densities is used at start.py needed for a flow density diagram in Plotter.py
        # ToDo reset flow, steps to zero again for new run
        :return:
        """
        self.density_list.append(analyzer.get_simulation().get_density())
        self.singleFlows.append(analyzer.get_traffic_flow_all_lanes())

    # ToDo move to start.py
    def finalize(self):
        """
        use when all single runs simulation with a density are done
        # ToDo reset flow, steps to zero again for new run
        :return:
        """
        self.avg_flows.append(np.mean(self.singleFlows))
        self.std_err_singleFlows.append(np.std(self.singleFlows, ddof=0))

    """
    Analyzes single simulations with a given density. Use it when a loop with different densities is used at start.py
    needed for a flow density diagram in Plotter.py
    """
