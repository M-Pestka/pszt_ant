from ant_colony import ant_colony
from graph import sparse_graph


if(__name__ == '__main__'):
    print('test klasy ant_colony')
    print('klasa będzie testowana na oko')
    colony = ant_colony(3)
    graph = sparse_graph(3)
    graph.set_edge(0, 1, 1.)
    graph.set_edge(1, 2, 1.)

    colony.set_problem(0, 2, graph)

    path_len = colony.calculate_path_len([0, 1, 2])
    assert path_len == 2., print(path_len)

    colony.simulate()
    print(colony.get_pheromone_graph())

    colony = ant_colony(3)
    graph = sparse_graph(3)
    graph.set_edge(0, 1, 1.)
    graph.set_edge(1, 2, 1.)
    graph.set_edge(0, 2, 1.5)

    print(graph._graph)
    colony.set_problem(0, 2, graph)

    colony.simulate()
    print(colony.get_pheromone_graph())