import sys
import time

from Analyse.AnalyzerSingleSim import *
from movementLogic.MyTrafficSimulation import *
from plotAndVisualize import Plotter
from StreetAttributes.tileAttrSetting import *
from Analyse.collisionChecker import CollisionChecker
from configuration.config import ConfigPreference
from preferences.PreferenceNV import Preferences

# select what visualization should be started. Use the console to give argument
# selection 1   debug scenario. Visualizes each vehicle movement step by step and the whole street. No probabilities
# selection 2   movement simulation with fixed street for 0.8 steps/sec. No probabilities
#               only on console. Save before running. Use full-screen
# selection 3   Depreciated
#               movement focused on one vehicle and portion of the street behind and ahead. No probabilities
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
# selection 9   like selection 8 but motorcyclist consider speed adjustments according to its preferences
#               Plots 2D-Pixel Plot
# selection 10  like selection 9, motorcyclist orient to its partners and preferences. Plots flow-density diagram
#               for street with curvature and speed limit for each density. Use selection 9
#               if movement should be visualized only and for 2D-Pixel Plot

if len(sys.argv) == 2:
    selection = int(sys.argv[1])
else:
    selection = 10  # ToDo change to selection which should be run on IDE

# ---------------------------------- selection 1 ------------------------------------
if selection == 1:
    print('Selection Mode: ', selection)
    cfg = ConfigPreference('selection_1')
    sim = TrafficSimulation(**cfg.model_settings)
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
    cfg = ConfigPreference('selection_2')
    sim = TrafficSimulation(**cfg.model_settings)
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
    cfg = ConfigPreference('selection_3')
    sim = TrafficSimulation(**cfg.model_settings)
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
    cfg = ConfigPreference('selection_4')
    sim = TrafficSimulation(**cfg.model_settings)
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

    print('\n', 'Length:         ', cfg.model_settings['length'], '\n',
          'Number_vehicles:', sim.get_number_total_vehicles(), '\n',
          'Density:        ', cfg.model_settings['density'], '\n',
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
    cfg = ConfigPreference('selection_5')

    # what densities shall be calculated. Lowest density should be number of bikers, which is fixed
    lowest_density = \
        (cfg.model_settings['platoon_size'] * cfg.model_settings['number_platoons']) / cfg.model_settings['length']
    density_list = np.linspace(lowest_density, 2, 15)

    avgFlows = []
    stdFlows = []

    for density in density_list:
        singleFlows = []
        cfg.model_settings['density'] = density
        sim = TrafficSimulation(**cfg.model_settings)
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
    cfg = ConfigPreference('selection_6')
    sim = TrafficSimulation(**cfg.model_settings)
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
    cfg = ConfigPreference('selection_7')
    sim = TrafficSimulation(**cfg.model_settings)
    sim.initialize()
    checker = CollisionChecker(sim)
    vis = VisualizeStreet(sim)
    tileAttrSetting = TileAttributeSetter(sim, cfg, modus='sinus', generate=True, amplitude=7, frequency=0.2)

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
    cfg = ConfigPreference('selection_8')
    sim = TrafficSimulation(**cfg.model_settings)
    sim.initialize()
    checker = CollisionChecker(sim)
    vis = VisualizeStreet(sim)
    analyzer = AnalyzerSingleSim(sim)
    tileAttrSetting = TileAttributeSetter(sim, cfg, modus='sinus_half', generate=True, amplitude=5000, frequency=0.1)

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


# ---------------------------------- selection 9 ------------------------------------
elif selection == 9:
    print('Selection Mode: ', selection)
    cfg = ConfigPreference('default')
    pref = Preferences(cfg)
    sim = TrafficSimulation(**cfg.model_settings)
    sim.set_config_object(cfg)
    sim.set_preference_object(pref)
    sim.initialize()
    checker = CollisionChecker(sim)
    vis = VisualizeStreet(sim)
    analyzer = AnalyzerSingleSim(sim)

    # street with constant curvature or half sinus or constant curvature
    tileAttrSetting = TileAttributeSetter(sim, cfg, modus='constant', generate=True, constant_curvature=601)
    # tileAttrSetting = TileAttributeSetter(sim, cfg, modus='step_function', generate=True, amplitude=601, frequency=0.03)

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
    focus_vehicle.set_symbol('X')

    for i in range(0, sim.total_amount_steps):
        checker.check_for_inconsistencies()
        vis.traffic_vis_tiles_granular()
        # time.sleep(0.8)
        # vis.traffic_vis_tiles_fix_lines_focused(focus_vehicle, display_curve=True)
        sim.moving(vis)
        # sim.moving(vis, vis_modus='step')
        analyzer.update()

    for lane in range(0, sim.get_lanes() + 1):
        Plotter.time_space_granular(vis.get_time_space_data(lane))

    analyzer.save_results()
    sys.stdout.write('\n')
    sys.stdout.write('\n')
    sys.stdout.write('\n')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of collisions:        {checker.number_of_collisions}')
    sys.stdout.write('\n')
    sys.stdout.write(f'number of missing index:     {checker.number_of_missing_pos}')
    sys.stdout.write('\n')
    sys.stdout.write(f'all vehicles present:        {checker.all_vehicle_present}')
    sys.stdout.write('\n')

# ---------------------------------- selection 10 ------------------------------------
elif selection == 10:
    print('Selection Mode: ', selection)
    cfg = ConfigPreference('default')
    pref = Preferences(cfg)

    # what densities shall be calculated. Lowest density should be number of bikers, which is fixed
    lowest_density = \
        (cfg.model_settings['platoon_size'] * cfg.model_settings['number_platoons']) / cfg.model_settings['length']
    density_list = np.linspace(lowest_density, 2, 10)

    avgFlows = []
    stdFlows = []

    for density in density_list:
        singleFlows = []
        cfg.model_settings['density'] = density

        sim = TrafficSimulation(**cfg.model_settings)
        sim.set_config_object(cfg)
        sim.set_preference_object(pref)
        sim.initialize()
        checker = CollisionChecker(sim)
        vis = VisualizeStreet(sim)
        analyzer = AnalyzerSingleSim(sim)

        tileAttrSetting = TileAttributeSetter(sim, cfg, modus='constant', generate=True, constant_curvature=401)
        # tileAttrSetting = TileAttributeSetter(sim, cfg, modus='sinus_half', generate=True, amplitude=5000, frequency=0.1)

        # shows how initial distribution of vehicles are for each density
        vis.traffic_vis_tiles()

        # for each density, the simulation will be run x times to get a variance
        for i in range(0, 20):
            for i in range(0, sim.total_amount_steps):
                checker.check_for_inconsistencies()
                vis.traffic_vis_tiles_granular()
                sim.moving(vis)
                analyzer.update()

            singleFlows.append(analyzer.get_traffic_flow_all_lanes())
            # uncomment if saving results for plotting flow-density diagram necessary
            analyzer.save_results(f'_density_{density}')

            # Plots different graphics for analysis. Problem: plotter overwrites stuff.
            # fun time series is defined for only one density and no inner loop
            # Plotter.fun_distro_diagram(analyzer.get_vehicle_summary_dict(), plot_type='Fun_Distribution_Motorcyclist')

            # Plots Time-Distance Diagram for Motorcyclists and Cars as well as the velocity Distribution
            # Plotter.time_distance_diagram(analyzer.get_vehicle_summary_dict(),
            #                               plot_type="Time_Distance_Diagram_Motorcyclist")
            # Plotter.time_distance_diagram(analyzer.get_vehicle_summary_dict(), plot_type="Time_Distance_Diagram_Car")
            # Plotter.velocity_distro_diagram(analyzer.get_vehicle_summary_dict(),
            #                                 plot_type='Velocity_Distribution_Motorcyclist')

        avgFlows.append(np.mean(singleFlows))
        stdFlows.append(np.std(singleFlows, ddof=0))

        sys.stdout.write('\n')
        sys.stdout.write('\n')
        sys.stdout.write('\n')
        sys.stdout.write('\n')
        sys.stdout.write(f'density:                     {density}')
        sys.stdout.write('\n')
        sys.stdout.write(f'number of collisions:        {checker.number_of_collisions}')
        sys.stdout.write('\n')
        sys.stdout.write(f'number of missing index:     {checker.number_of_missing_pos}')
        sys.stdout.write('\n')
        sys.stdout.write(f'all vehicles present:        {checker.all_vehicle_present}')
        sys.stdout.write('\n')

    # Flow Density Diagram needs std error. Change density_list as well as inner for loop
    Plotter.flow_density_diagram_errorbar(density_list, avgFlows, stdFlows)

    # fun time series is defined for only one density and no inner loop
    # Plotter.fun_distro_diagram(analyzer.get_vehicle_summary_dict(), plot_type='Fun_Distribution_Motorcyclist')
    print(avgFlows)
