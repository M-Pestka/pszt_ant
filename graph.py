from copy import deepcopy
from abc import ABCMeta, abstractmethod
import numpy as np

class graph(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_neighbours(self):
        pass

    @abstractmethod
    def get_edge_value(self):
        pass
    @abstractmethod
    def reset(self):
        pass
    

class sparse_graph(graph):
    def __init__(self, num_verteces, default_value=np.inf):
        # można pozostawić niezainicjalizowane ale wymagałoby to
        # skomplikowanej obsługi
        super().__init__()
        self._graph = {i:{} for i in range(num_verteces)}
        self.default_value = default_value
        self.num_verteces = num_verteces

    def get_neighbours(self, vertex):
        assert vertex < self.num_verteces
        return deepcopy(list(self._graph.get(vertex, {}).keys()))

    def get_edge_value(self, src_vertex, dst_vertex):
        assert src_vertex < self.num_verteces and dst_vertex < self.num_verteces
        return deepcopy(self._graph.get(src_vertex, {}).get(dst_vertex, self.default_value))

    def set_edge(self, src_vertex, dst_vertex, value):
        assert src_vertex < self.num_verteces and dst_vertex < self.num_verteces
        self._graph[src_vertex][dst_vertex] = value
        self._graph[dst_vertex][src_vertex] = value

    def reset(self):
        self._graph = {i:{} for i in range(self.num_verteces)}


class pheromone_graph(sparse_graph):

    def multiply(self, multiplier):
        self.default_value *= multiplier
        for i in range(self.num_verteces):
            self._graph[i].update({n: multiplier * self._graph[i][n] for n in self._graph[i].keys()})

    def add_to_edge(self, src_vertex, dst_vertex, value):
        tmp = self._graph[src_vertex].get(dst_vertex, self.default_value) + value
        self._graph[src_vertex][dst_vertex] = tmp
        self._graph[dst_vertex][src_vertex] = tmp

    def __repr__(self):
        return str(self._graph)

