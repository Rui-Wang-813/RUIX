import unittest
import Graph as gs

class TestGraphSearch(unittest.TestCase):

    def setUp(self) -> None:
        g = gs.Graph()
        g.addEdge(0, 1)
        g.addEdge(0, 2)
        g.addEdge(2, 3)
        self.graph = g

        return super().setUp()
    
    def test_dfs(self) -> None:
        path = self.graph.dfs(2)
        self.assertEqual(path, [2,3,0,1])
    
    def test_bfs(self) -> None:
        path = self.graph.bfs(2)
        self.assertEqual(path, [2,0,3,1])

if __name__ == '__main__':
    unittest.main()