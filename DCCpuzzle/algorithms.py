# src/algorithms.py

import time
from collections import deque

from multi_node import MultiNode
from multi_binary_heap import MultiBinaryHeap
from puzzle import Puzzle15State

class SearchResult:
    # NO MODIFICAR
    def __init__(self, path, expansions, elapsed_ms):
        # path: lista de MultiNode desde inicial hasta meta
        self.path = path
        self.expansions = expansions
        self.elapsed_ms = elapsed_ms

class BaseSearch:
    # NO MODIFICAR
    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        raise NotImplementedError

class BFS(BaseSearch):
    def solve(self):
        root = MultiNode(self.problem.initial_state)
        frontier = deque([root])
        explored = set()
        expansions = 0
        goal_node = None

        t0 = time.time()

        while frontier:
            node = frontier.popleft()
            if node.state.is_goal():
                goal_node = node
                break
            expansions += 1
            explored.add(node.state)

            for succ_state, action, cost, _ in node.state.h_successors(lambda s: 0):
                if succ_state in explored:
                    continue
                child = MultiNode(succ_state, parent=node, action=action)
                frontier.append(child)

        elapsed_ms = (time.time() - t0) * 1000

        # reconstrucción del camino
        path = []
        cur = goal_node
        while cur:
            path.append(cur)
            cur = cur.parent
        path.reverse()

        return SearchResult(path, expansions, elapsed_ms)



class DFS(BaseSearch):
    # NO MODIFICAR
    def solve(self):
        root = MultiNode(self.problem.initial_state)
        frontier = [root]
        explored = set()
        expansions = 0

        t0 = time.time()
        goal_node = None
        while frontier:
            node = frontier.pop()
            if node.state.is_goal():
                goal_node = node
                break
            expansions += 1
            explored.add(node.state)

            # h_successors(heuristic) -> (state, action, cost, h_dummy)
            succ = node.state.h_successors(lambda s: 0)
            for succ_state, action, cost, _ in succ:
                if succ_state in explored:
                    continue
                child = MultiNode(succ_state, parent=node, action=action)
                frontier.append(child)

        elapsed = (time.time() - t0) * 1000

        path = []
        cur = goal_node
        while cur:
            path.append(cur)
            cur = cur.parent
        path.reverse()
        return SearchResult(path, expansions, elapsed)

class AStar(BaseSearch):
    # Completar - Parte 2
    def __init__(self, problem, heuristic):
        super().__init__(problem)
        self.heuristic = heuristic
        # usaremos heap id=0 para f-values
        self.heap = MultiBinaryHeap(id=0) # puedes cambiarlo a la EDD que prefieras

    def solve(self):
        # nodo raíz
        root = MultiNode(self.problem.initial_state)
        root.g = 0
        root.h[0] = self.heuristic(root.state)
        root.key[0] = root.g + root.h[0]

        # inicializar heap
        self.heap.clear()
        self.heap.insert(root)

        # inicializar contadores y estructuras
        expansions = 0
        t0 = time.time()
        goal_node = None

        while not self.heap.is_empty():
            # Completar - Parte 2
            pass

        # reconstruir camino
        path = []
        cur = goal_node
        while cur:
            path.append(cur)
            cur = cur.parent
        path.reverse()
        return SearchResult(path, expansions, elapsed)