
from graph import pheromone_graph


class ant_colony:

    def __init__(self, num_verteces):
        self.single_pheromone_value = 0.2
        self.pheromone_graph = pheromone_graph(num_verteces)


    def _sim_single_ant(self):
        path = self._randomize_path()
        path_len = self.calculate_path_len(path)
        for src, dst in zip(path[:-1], path[1:]):
            self.pheromone_graph.add_to_edge(src, dst, self.single_pheromone_value/path_len)

    def simulate(self, num_ants, time_out_iter = 10000):
        converged = False
        i = 0
        while(not converged and i < time_out_iter):
            i+=1
            self._sim_single_ant()
            converged = self.check_conversion()

        return converged

    def _randomize_path(self):
        raise Exception('Not implemented')

    def reset(self):
        raise Exception('Not implemented')

    def _make_intersection_decision(self):
        raise Exception('Not implemented')

    def check_conversion(self):
        raise Exception('Not implemented')

    def calculate_path_len(self, path):
        raise Exception('Not implemented')