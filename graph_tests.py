import unittest
from graph import sparse_graph, pheromone_graph

class TestSum(unittest.TestCase):

    def test_sparse_graph(self):
        g = sparse_graph(3)
        g.set_edge(1, 2, 1.)
        self.assertEqual(1., g.get_edge_value(1, 2))
        g.set_edge(1, 2, 2.)
        self.assertEqual(2., g.get_edge_value(1, 2))

        self.assertEqual([2], g.get_neighbours(1), 'test1')
        self.assertEqual([], g.get_neighbours(0), 'test2')
        g.set_edge(0, 2, 2)
        self.assertEqual(set([1, 0]), set(g.get_neighbours(2)), 'test3')

    def test_sum_tuple(self):
        g = pheromone_graph(3)
        g.set_edge(1, 2, 1.)
        self.assertEqual(1., g.get_edge_value(1, 2))
        g.set_edge(1, 2, 2.)
        self.assertEqual(2., g.get_edge_value(1, 2))
        g.multiply(.5)
        self.assertEqual(1., g.get_edge_value(1, 2))

        self.assertEqual(g.get_neighbours(1), [2])
        self.assertEqual(g.get_neighbours(0), [])
        g.set_edge(0, 2, 2)
        self.assertEqual(set([1, 0]), set(g.get_neighbours(2)))

        g2 = pheromone_graph(3, default_value=1.)
        self.assertEqual(1., g2.get_edge_value(1, 2))
        g2.multiply(3.)
        self.assertEqual(3., g2.get_edge_value(2, 0))
        g2.add_to_edge(1, 2, 1.)
        self.assertEqual(4., g2.get_edge_value(1, 2))

        g2.normalize()
        self.assertEqual(1., g2.get_edge_value(1, 2))

if __name__ == '__main__':
    unittest.main()