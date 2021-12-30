
from typing import List
from queue import PriorityQueue


class Graph:

    def __init__(self, graph: List[List[int]]) -> None:
        self.graph = graph
        self.V = len(graph)
    
    def add_edge(self, u: int, v: int, weight: int) -> None:
        self.graph[u][v] = self.graph[v][u] = weight
    
    def dijsktra_search(self, s: int) -> None:
        visited = [False] * self.V
        dist = [float('inf')] * self.V

        dist[s] = 0

        # nested function to find the node with currently smallest distance to source.
        def min_distance() -> int:
            return min([i for i in range(self.V) if not visited[i]], key=lambda i: dist[i])
        
        for _ in range(self.V):
            u = min_distance()
            visited[u] = True

            for v in range(self.V):
                if (not visited[v]) and self.graph[u][v] > 0 \
                    and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]

        # helper function to print out the result.
        def printSolution():
            print("Vertex \tDistance from Source")
            for node in range(self.V):
                print(node, "\t", dist[node])
        
        printSolution()
    
    def a_star_search(self, s: int, t: int, heur=lambda u: 0) -> None:
        frontier = PriorityQueue()
        frontier.put(s, heur(s))

        dist = [float('inf') for _ in range(self.V)]
        dist[s] = 0

        while (not frontier.empty()):
            u = frontier.get()

            if u == t:
                break
            
            for v in range(self.V):
                if self.graph[u][v]:
                    new_dist = dist[u] + self.graph[u][v]
                    if new_dist < dist[v]:
                        frontier.put(v, heur(v) + new_dist)
                        dist[v] = new_dist

_g = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
        [4, 0, 8, 0, 0, 0, 0, 11, 0],
        [0, 8, 0, 7, 0, 4, 0, 0, 2],
        [0, 0, 7, 0, 9, 14, 0, 0, 0],
        [0, 0, 0, 9, 0, 10, 0, 0, 0],
        [0, 0, 4, 14, 10, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 1, 6],
        [8, 11, 0, 0, 0, 0, 1, 0, 7],
        [0, 0, 2, 0, 0, 0, 6, 7, 0]
        ]
graph = Graph(_g)
graph.dijsktra_search(0)