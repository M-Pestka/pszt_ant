import argparse
from graph import pandas_graph
from utils import load_network
from ant_colony import ant_colony

if(__name__ =='__main__'):

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', help = 'path', type = str, required=True)
    parser.add_argument('-s', help = 'source', type = str, required= True)
    parser.add_argument('-d', help = 'destination', type = str, required=True)

    args = parser.parse_args()

    path = args.p
    src = args.s
    dst = args.d

    src_name = src
    dst_name = dst

    verteces, dataframe = load_network(path)
    num_verteces = len(verteces)

    graph = pandas_graph(dataframe, num_verteces = num_verteces )

    src = graph._decode_vertex(src)
    dst = graph._decode_vertex(dst)
    
    solver = ant_colony(num_verteces)

    solver.set_problem(src, dst, graph)
    solver.simulate()

    print(solver.get_pheromone_graph())

    pheromone_graph = solver.get_pheromone_graph()

    name_map = {r['name']: (r['lat'], r['lon']) for i, r in verteces.iterrows()}

    MAX_COST = pheromone_graph.max()

    import matplotlib.pyplot as plt
    for i, row in dataframe.iterrows():
        p1 = name_map[row['source']]
        p2 = name_map[row['target']]
        cost = pheromone_graph.get_edge_value(graph._decode_vertex(row['source']), graph._decode_vertex(row['target']))
        plt.plot([p1[1], p2[1]], [p1[0], p2[0]], c='gray', linewidth=float(cost) / MAX_COST)

    plt.scatter(x=verteces.lon, y=verteces.lat)
    for n ,x, y in zip(verteces.name, verteces.lon, verteces.lat):
        plt.annotate( n, (x, y))

    plt.show()