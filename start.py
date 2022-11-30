import sys
import time

import numpy as np
from vehicles.Vehicles import *
from vehicles import Motorcycle
from AnalyzerSingleSim import *
from MyTrafficSimulation import *
import Plotter
from tileAttrSetting import *
from collisionChecker import CollisionChecker

# select what visualization should be started. Use the console to give argument
# selection 1   debug scenario. Visualizes each vehicle movement step by step and the whole street. No probabilities
# selection 2   movement simulation with fixed street for 0.8 steps/sec. No probabilities
#               only on console. Save before running. Use full-screen
# selection 3   movement focused on one vehicle and portion of the street behind and ahead. No probabilities
#               only on console. Save before running. Use full-screen
# selection 4   calculates a single average flow-density
# selection 5   plots a flow-density diagram in an error bar
# selection 6   like selection 1 but plotting is more granular for each side separately. 2D Pixel Plot
# selection 7   Tile setting with curvature
# selection 8   Tile setting with curvature and Motorcyclist simple speed_up and slow_down logic.
#               Motorcyclist do not overtake Platoon member if on same lane
#               Visualization with one vehicle focused
#               saves an attribute dict s.t. it can be filled with speed limit and curvature
#               visualizes time distance time-line diagram of motorcyclist and cars
#               visualizes velocity distribution of motorcyclists


if len(sys.argv) == 2:
    selection = int(sys.argv[1])
else:
    selection = 8  # ToDo change to selection which should be run on IDE

# ---------------------------------- selection 1 ------------------------------------
if selection == 1:
    print('Selection Mode: ', selection)
    # Has to be set in class Trafficsimulation again
    model_settings = {
        'length': 40,  # don't use more than 50 for visualization as console cannot display more at once
        'density': 0.5,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': -1,
        'prob_changelane': 1,
        'car_share': 0.9,
        'number_platoons': 3,
        'platoon_size': 3,
        'speed_preferences': {
            'cautious': None,
            'average': None,
            'speed': None,
        },
        'total_amount_steps': 10
    }

    sim = TrafficSimulation(**model_settings)
    sim.initialize()
    checker = CollisionChecker(sim)
    vis = VisualizeStreet(sim)

    # initial setup visualization
    vis.traffic_vis_tiles()

    # visualizes each step by step with move and switching
    for i in range(0, sim.total_amount_steps):
        checker.check_for_inconsistencies()
        sim.moving(vis, vis_modus='step')

    sys.stdout.write('\n')
    sys.stdout.write(f'number of collisions:        {checker.number_of_collisions}')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of missing index:     {checker.number_of_missing_pos}')
    sys.stdout.write('\n')
    sys.stdout.write(f'all vehicles present:        {checker.all_vehicle_present}')
    sys.stdout.write('\n')

# ---------------------------------- selection 2 ------------------------------------
elif selection == 2:
    print('Selection Mode: ', selection)
    model_settings = {
        'length': 20,  # don't use more than 50 for visualization as console cannot display more at once
        'density': 1,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.1,
        'prob_changelane': 0.5,
        'car_share': 0.9,
        'number_platoons': 1,
        'platoon_size': 3,
        'speed_preferences': {
            'cautious': None,
            'average': None,
            'speed': None,
        },
        'total_amount_steps': 100
    }

    sim = TrafficSimulation(**model_settings)
    sim.initialize()
    checker = CollisionChecker(sim)
    vis = VisualizeStreet(sim)

    for i in range(0, sim.total_amount_steps):
        checker.check_for_inconsistencies()
        vis.traffic_vis_tiles_fix_lines(display_curve=True)
        time.sleep(1)
        sim.moving(vis)

    sys.stdout.write('\n')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of collisions:        {checker.number_of_collisions}')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of missing index:     {checker.number_of_missing_pos}')
    sys.stdout.write('\n')
    sys.stdout.write(f'all vehicles present:        {checker.all_vehicle_present}')
    sys.stdout.write('\n')

# ---------------------------------- selection 3 ------------------------------------
elif selection == 3:
    print('Selection Mode: ', selection)
    model_settings = {
        'length': 50,
        'density': 0.5,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': -1,
        'prob_changelane': 1,
        'car_share': 0.9,
        'number_platoons': 1,
        'platoon_size': 1,
        'speed_preferences': {
            'cautious': None,
            'average': None,
            'speed': None,
        },
        'total_amount_steps': 100
    }

    sim = TrafficSimulation(**model_settings)
    sim.initialize()
    checker = CollisionChecker(sim)
    vis = VisualizeStreet(sim)

    # choose which vehicle should be focused on
    vis.traffic_vis_tiles()

    print('select vehicle to focus on (choose: (idx, lane) ')
    vehicle_dict = {}
    for idx, vehicle in enumerate(sim.vehicle_list):
        vehicle_dict[idx] = vehicle

    for key, value in vehicle_dict.items():
        index = vehicle_dict[key].get_tile().get_index()
        lane = vehicle_dict[key].get_tile().get_lane()
        print(f'{key}: {index, lane}')

    chosen_vehicle_number = input()
    focus_vehicle = vehicle_dict[int(chosen_vehicle_number)]

    for i in range(0, sim.total_amount_steps):
        checker.check_for_inconsistencies()
        time.sleep(1.1)
        vis.traffic_vis_tiles_fix_lines_focused(focus_vehicle, display_curve=True)
        sim.moving(vis)

    sys.stdout.write('\n')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of collisions:        {checker.number_of_collisions}')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of missing index:     {checker.number_of_missing_pos}')
    sys.stdout.write('\n')
    sys.stdout.write(f'all vehicles present:        {checker.all_vehicle_present}')
    sys.stdout.write('\n')

# ---------------------------------- selection 4 ------------------------------------
elif selection == 4:
    print('Selection Mode: ', selection)
    model_settings = {
        'length': 40,
        'density': 2,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.2,
        'prob_changelane': 0.5,
        'car_share': 0.9,
        'number_platoons': 1,
        'platoon_size': 3,
        'speed_preferences': {
            'cautious': None,
            'average': None,
            'speed': None,
        },
        'total_amount_steps': 100
    }

    sim = TrafficSimulation(**model_settings)
    sim.initialize()
    checker = CollisionChecker(sim)
    analyzer = AnalyzerSingleSim(sim)
    vis = VisualizeStreet(sim)
    # vis.traffic_vis_tiles()

    flows = []
    number_of_loops = 10
    for i in range(0, number_of_loops):
        for step in range(0, sim.total_amount_steps):
            checker.check_for_inconsistencies()
            sim.moving()
            # vis.traffic_vis_tiles()
            analyzer.update()
        flows.append(analyzer.get_traffic_flow_all_lanes())

    print('\n', 'Length:         ', model_settings['length'], '\n',
          'Number_vehicles:', sim.get_number_total_vehicles(), '\n',
          'Density:        ', model_settings['density'], '\n',
          'number of loops:', number_of_loops, '\n',
          'Flows:          ', flows, '\n',
          'avg flow:       ', sum(flows) / len(flows), '\n',
          'std_flow:       ', np.std(flows))
    print('----------------------------------------------------------')

    sys.stdout.write('\n')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of collisions:        {checker.number_of_collisions}')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of missing index:     {checker.number_of_missing_pos}')
    sys.stdout.write('\n')
    sys.stdout.write(f'all vehicles present:        {checker.all_vehicle_present}')
    sys.stdout.write('\n')

# ---------------------------------- selection 5 ------------------------------------
elif selection == 5:
    print('Selection Mode: ', selection)
    model_settings = {
        'length': 100,
        'density': 0.2,  # Hint will be changed in selection 5
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.2,
        'prob_changelane': 0.5,
        'car_share': 0.9,
        'number_platoons': 3,  # Hint will be adjusted in selection 5
        'platoon_size': 3,  # Hint will be adjusted in selection 5
        'speed_preferences': {
            'cautious': None,
            'average': None,
            'speed': None,
        },
        'total_amount_steps': 100
    }

    # what densities shall be calculated. Lowest density should be number of bikers, which is fixed
    lowest_density = (model_settings['platoon_size'] * model_settings['number_platoons']) / model_settings['length']
    density_list = np.linspace(lowest_density, 2, 15)

    avgFlows = []
    stdFlows = []

    for density in density_list:
        singleFlows = []
        model_settings['density'] = density
        sim = TrafficSimulation(**model_settings)
        sim.initialize()
        checker = CollisionChecker(sim)
        analyzer = AnalyzerSingleSim(sim)
        vis = VisualizeStreet(sim)
        # vis.traffic_vis_tiles()

        # for each density, the simulation will be run 10 times to get a variance
        for i in range(0, 10):

            for step in range(0, sim.total_amount_steps):
                # checker.check_for_inconsistencies()
                sim.moving()
                # vis.traffic_vis_tiles()
                analyzer.update()

            singleFlows.append(analyzer.get_traffic_flow_all_lanes())

        avgFlows.append(np.mean(singleFlows))
        stdFlows.append(np.std(singleFlows, ddof=0))

        # sys.stdout.write('\n')
        # sys.stdout.write('\n')
        # sys.stdout.write(f'number of collisions:        {checker.number_of_collisions}')
        # sys.stdout.write('\n')
        # sys.stdout.write(f'number of missing index:     {checker.number_of_missing_pos}')
        # sys.stdout.write('\n')
        # sys.stdout.write(f'all vehicles present:        {checker.all_vehicle_present}')

    Plotter.flow_density_diagram_errorbar(density_list, avgFlows, stdFlows)
    print(avgFlows)

# ---------------------------------- selection 6 ------------------------------------
elif selection == 6:
    print('Selection Mode: ', selection)
    model_settings = {
        'length': 100,
        'density': 0.5,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.1,
        'prob_changelane': 0.5,
        'car_share': 0.9,
        'number_platoons': 1,
        'platoon_size': 3,
        'speed_preferences': {
            'cautious': None,
            'average': None,
            'speed': None,
        },
        'total_amount_steps': 100
    }

    sim = TrafficSimulation(**model_settings)
    sim.initialize()
    checker = CollisionChecker(sim)
    vis = VisualizeStreet(sim)

    for i in range(0, sim.total_amount_steps):
        checker.check_for_inconsistencies()
        vis.traffic_vis_tiles_granular()
        sim.moving(vis)

    for lane in range(0, sim.get_lanes() + 1):
        Plotter.time_space_granular(vis.get_time_space_data(lane))

    sys.stdout.write('\n')
    sys.stdout.write(f'number of collisions:        {checker.number_of_collisions}')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of missing index:     {checker.number_of_missing_pos}')
    sys.stdout.write('\n')
    sys.stdout.write(f'all vehicles present:        {checker.all_vehicle_present}')
    sys.stdout.write('\n')

# ---------------------------------- selection 7 ------------------------------------
elif selection == 7:
    print('Selection Mode: ', selection)
    model_settings = {
        'length': 30,
        'density': 0.5,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.1,
        'prob_changelane': 0.2,
        'car_share': 0.9,
        'number_platoons': 1,
        'platoon_size': 3,
        'speed_preferences': {
            'cautious': None,
            'average': None,
            'speed': None,
        },
        'total_amount_steps': 2
    }

    sim = TrafficSimulation(**model_settings)
    sim.initialize()
    checker = CollisionChecker(sim)
    vis = VisualizeStreet(sim)
    tileAttrSetting = TileAttributeSetter(sim, modus='sinus', generate=True, amplitude=7, frequency=0.2)

    vis.traffic_vis_tiles(display_curve=True)

    for i in range(0, sim.total_amount_steps):
        checker.check_for_inconsistencies()
        sim.moving(vis)

    sys.stdout.write('\n')
    sys.stdout.write(f'number of collisions:        {checker.number_of_collisions}')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of missing index:     {checker.number_of_missing_pos}')
    sys.stdout.write('\n')
    sys.stdout.write(f'all vehicles present:        {checker.all_vehicle_present}')
    sys.stdout.write('\n')

# ---------------------------------- selection 8 ------------------------------------
elif selection == 8:
    print('Selection Mode: ', selection)
    model_settings = {
        'length': 1000,
        'density': 0.1,
        'num_lanes': 1,  # [0,1] do not change
        'prob_slowdown': 0.1,
        'prob_changelane': 1,
        'car_share': 1,
        'number_platoons': 1,
        'platoon_size': 4,
        'speed_preferences': {
            'cautious': None,
            'average': None,
            'speed': None,
        },
        'total_amount_steps': 100
    }

    sim = TrafficSimulation(**model_settings)
    sim.initialize()
    checker = CollisionChecker(sim)
    vis = VisualizeStreet(sim)
    analyzer = AnalyzerSingleSim(sim)
    tileAttrSetting = TileAttributeSetter(sim, modus='sinus_half', generate=True, amplitude=5000, frequency=0.1)

    # choose which vehicle should be focused on
    vis.traffic_vis_tiles()

    print('select vehicle to focus on (choose: (idx, lane) ')
    vehicle_dict = {}
    for idx, vehicle in enumerate(sim.vehicle_list):
        vehicle_dict[idx] = vehicle

    for key, value in vehicle_dict.items():
        index = vehicle_dict[key].get_tile().get_index()
        lane = vehicle_dict[key].get_tile().get_lane()
        print(f'{key}: {index, lane}')

    chosen_vehicle_number = input()
    focus_vehicle = vehicle_dict[int(chosen_vehicle_number)]
    # focus_vehicle.set_symbol('X') For Visualization only

    for i in range(0, sim.total_amount_steps):
        checker.check_for_inconsistencies()
        # time.sleep(1.1)
        # vis.traffic_vis_tiles_fix_lines_focused(focus_vehicle, display_curve=True)
        sim.moving(vis)
        analyzer.update()

    Plotter.time_distance_diagram(analyzer.get_vehicle_summary_dict(), plot_type="Time_Distance_Diagram_Motorcyclist")
    Plotter.time_distance_diagram(analyzer.get_vehicle_summary_dict(), plot_type="Time_Distance_Diagram_Car")
    Plotter.velocity_distro_diagram(analyzer.get_vehicle_summary_dict(), plot_type='Velocity_Distribution_Motorcyclist')

    sys.stdout.write('\n')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of collisions:        {checker.number_of_collisions}')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of missing index:     {checker.number_of_missing_pos}')
    sys.stdout.write('\n')
    sys.stdout.write(f'all vehicles present:        {checker.all_vehicle_present}')
    sys.stdout.write('\n')


