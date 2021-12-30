from typing import List
from collections import defaultdict


class Graph:

    def __init__(self) -> None:
        self.graph = defaultdict(list)
    
    def addEdge(self,u,v):
        self.graph[u].append(v)
        self.graph[v].append(u)
    
    def dfs(self, u) -> List:
        visited = set()
        path = []
        stack = [u]

        while len(stack):
            node = stack.pop(-1)
            if node in visited:
                continue
            path.append(node)
            visited.add(node)
            stack.extend(self.graph[node])

        return path

    def bfs(self, u) -> List:
        visited = set([u])
        path = []
        queue = [u]

        while len(queue):
            node = queue.pop(0)
            path.append(node)
            
            for v in self.graph[node]:
                if v not in visited:
                    visited.add(v)
                    queue.append(v)

        return path        