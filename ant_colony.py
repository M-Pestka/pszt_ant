from copy import deepcopy

import numpy as np
from graph import pheromone_graph


class ant_colony:

    def __init__(self, num_verteces, single_pheromone_value = 0.2, pheromone_multiplier = 0.99):
        self.single_pheromone_value = single_pheromone_value
        self.pheromone_graph = pheromone_graph(num_verteces, 1.)
        self.problem_set = False
        self.pheromone_multiplier = pheromone_multiplier

    def set_problem(self, source, destination, graph):
        self.problem_set = True
        self.src = source
        self.dst = destination
        self.distance_graph = graph


    def _sim_single_ant(self):
        # symulacja pojedynczej mrowki
        try:
            path = self._randomize_path()
            path_len = self.calculate_path_len(path)
            for src, dst in zip(path[:-1], path[1:]):
                self.pheromone_graph.add_to_edge(src, dst, self.single_pheromone_value/path_len)
                self.pheromone_graph.multiply(self.pheromone_multiplier)
        except:
            pass

    def simulate(self, time_out_iter = 10000):
        converged = False
        i = 0
        while(not converged and i < time_out_iter):
            i+=1
            self._sim_single_ant()
            converged = self.check_conversion()

        return converged

    def _randomize_path(self):
        visited = []
        visited.append(self.src)
        while(visited[-1] != self.dst):
            move = self._make_intersection_decision(visited)
            visited.append(move)
        return visited

    def reset(self):
        self.pheromone_graph.reset()
        self.distance_graph.reset()

    def _make_intersection_decision(self, visited):
        posibilities = set(self.distance_graph.get_neighbours(visited[-1])).difference(set(visited))
        posibilities = list(posibilities)

        if(len(posibilities) <= 0):
            raise Exception('slepa uliczka')

        proba = [self.pheromone_graph.get_edge_value(visited[-1], scnd_vertex) for scnd_vertex in posibilities]
        proba /= np.sum(proba)
        return np.random.choice(posibilities, p = proba)


    def check_conversion(self):
        return False # we do not know the apropriate conversion condition

    def calculate_path_len(self, path):
        val = 0.
        for src, dst in zip(path[:-1], path[1:]):
            val += self.distance_graph.get_edge_value(src, dst)

        return val

    def get_pheromone_graph(self):
        return deepcopy(self.pheromone_graph)