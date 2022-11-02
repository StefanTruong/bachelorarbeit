def visualizations(densities, number_lanes):
    '''
    Visualize the output of the model as the relationship between density and
    average flow rate.
    '''
    mean_flows = []
    std_flows = []

    for dens in densities:
        flows = []
        for j in range(100):
            sim = TrafficSimulation(density=dens, num_lanes=number_lanes)
            sim.initialize()
            for i in range(50):
                sim.calculate()
            avg_flow = sim.flow / float(sim.step)
            flows.append(avg_flow)
        mean_flows.append(np.mean(flows) / float(number_lanes))
        std_flows.append(np.std(flows))

    plt.errorbar(scipy.linspace(0, 1, 50), mean_flows, xerr=0, yerr=1.96 * np.array(std_flows))
    plt.title('Traffic Flow over Density ({} Lane)'.format(number_lanes))
    plt.ylabel('Traffic Flow')
    plt.xlabel('Car Density')
    plt.show()


visualizations(np.linspace(0, 1, 50), 1)
visualizations(np.linspace(0, 1, 50), 2)