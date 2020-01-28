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

    def max(self):
        def my_max(x):
            if(x == []):
                return 0.
            else:
                return max(x)


        return my_max(float(my_max(d.values())) for d in self._graph.values())

    def normalize(self):
        max = self.max()
        self._graph = {k:{k2: val/max for k2, val in v.items()} for k, v in self._graph.items() }

class pandas_graph(sparse_graph):
    def __init__(self, links_dataframe, num_verteces = None, default_value=np.inf):
        # można pozostawić niezainicjalizowane ale wymagałoby to
        # skomplikowanej obsługi
        if(num_verteces is None):
            num_verteces = len(links_dataframe.source.value_counts())

        super().__init__(num_verteces)
        self._graph = {i:{} for i in range(num_verteces)}
        self.default_value = default_value

        self.num_verteces = num_verteces

        self.coding = {}
        self.reverse_coding = {}
        # -1 bo jest inkrementowany przed dodaniem
        self.__max_vertex_index = -1

        for i, row in links_dataframe.iterrows():
            s = row['source']
            d = row['target']
            c = row['cost']
            s = self._decode_vertex(s)
            d = self._decode_vertex(d)
            c = float(c)

            self.set_edge(s, d, c)

        self.normalize()

    def _endoce_vertex(self, vertex_idx):
        return self.reverse_coding[vertex_idx]

    def _decode_vertex(self, vertex_str):
        if(not vertex_str in self.coding):
            self.__max_vertex_index += 1
            self.coding[vertex_str] = self.__max_vertex_index
            self.reverse_coding[self.__max_vertex_index] = vertex_str
        return self.coding[vertex_str]

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

