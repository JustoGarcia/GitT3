from multi_binary_heap import MultiBinaryHeap
from multi_node import MultiNode
from algorithms import SearchResult
import time
import numpy as np

class FocalSearch:
    def __init__(self, initial_state, inad_h, adm_h, weight=1):
        # NO MODIFICAR
        self.expansions = 0
        self.initial_state = initial_state
        self.weight = weight
        self.inad_h        = inad_h     # política: vector de 4
        self.adm_h         = adm_h      # heurística admisible: scalar
        self.open          = MultiBinaryHeap(0)
        self.preferred     = MultiBinaryHeap(1)
        self.generated     = {}

    def fvalue(self, g, h):
        # NO MODIFICAR
        return g + self.weight * h

    def solve(self):
        # MODIFICAR ESTO EN BASE A VERSIÓN DE FOCAL SEARCH
        #return self.heuristic_search(self.weight) # <-- para focal_search
        return self.discrepancy_search(self.weight) # <- para focal_discrepancy_search
    
    def heuristic_search(self, focal_w=1):
        
        # 1. Reiniciar métricas
        t0 = time.time()
        self.expansions = 0
        self.open.clear()
        self.preferred.clear()
        self.generated = {}

        # 2. Nodo raíz
        root = MultiNode(self.initial_state)
        root.g = 0
        root.h[0] = self.inad_h(self.initial_state)  # h_inad
        root.h[1] = self.adm_h(self.initial_state)   # h_adm
        root.key[0] = root.h[0]                      # clave para heap 0 (open): h_inad
        root.key[1] = self.fvalue(root.g, root.h[1]) # clave para heap 1 (focal): f_adm

        # 3. Insertar en heaps y registrar nodo
        self.open.insert(root)
        self.preferred.insert(root)
        self.generated[self.initial_state] = root

        # 4. Loop de expansión
        while not self.preferred.is_empty():
            # 4.1 timeout de 30 min
            if time.time() - t0 > 1800:
                print("TIME OUT")
                return SearchResult([], self.expansions, (time.time()-t0)*1000)

            # 4.2 obtener f_min
            f_min = self.open.top().key[1]

            # 4.3 extraer mejor nodo de preferred y remover de open
            node = self.preferred.extract()
            self.open.extract(node.heap_index[0])
            self.expansions += 1

            # 4.4 verificar objetivo
            if node.state.is_goal():
                elapsed = (time.time() - t0) * 1000
                return SearchResult(node.path(), self.expansions, elapsed)

            # 4.5 expandir sucesores
            for child_state, action, cost, _ in node.state.successors():
                g2 = node.g + cost
                child = self.generated.get(child_state)

                if child is None or g2 < child.g:
                    if child is None:
                        child = MultiNode(child_state)
                        self.generated[child_state] = child

                    child.parent = node
                    child.action = action
                    child.g = g2

                    # 4.6 calcular heurísticas
                    child.h[0] = self.inad_h(child_state)   # h_inad
                    child.h[1] = self.adm_h(child_state)    # h_adm

                    # 4.7 claves para heaps
                    child.key[0] = child.h[0]  # heap 0: ordenar por h_inad
                    child.key[1] = self.fvalue(child.g, child.h[1])  # heap 1: ordenar por f_adm

                    # 4.8 insertar en heaps
                    self.open.insert(child)
                    if child.key[1] <= focal_w * f_min:
                        self.preferred.insert(child)

        # 5. No se encontró solución
        elapsed = (time.time() - t0) * 1000
        return SearchResult([], self.expansions, elapsed)


    def discrepancy_search(self, focal_w=1): 
        # NO MODIFICAR
        """
        Focal Discrepancy Search (FDS(best)):
        - open list (self.open, heap 0) ordenada por f_adm = g + adm_h
        - focal list (self.preferred, heap 1) ordenada por discrepancias acumuladas
        """
        # 1) Reiniciar métricas y estructuras
        t0 = time.time()
        self.expansions = 0
        self.open.clear()
        self.preferred.clear()
        self.generated = {}

        # 2) Crear nodo raíz
        root = MultiNode(self.initial_state)
        root.g      = 0
        root.h[0]   = self.adm_h(self.initial_state)   # heurística admisible para el open
        root.key[0] = 0                                # discrepancias acumuladas
        root.key[1] = self.fvalue(root.g, root.h[0])   # f_adm = g + h_adm

        # 3) Insertar raíz en ambos heaps
        self.open.insert(root)
        self.preferred.insert(root)
        self.generated[self.initial_state] = root

        # 4) Bucle principal
        while not self.preferred.is_empty():
            # 4.1) timeout de suboptimalidad (30 min)
            if time.time() - t0 > 1800:
                print("TIME OUT")
                return SearchResult([], self.expansions, (time.time()-t0)*1000)

            # 4.2) f_min = mínimo f_adm en open
            f_min = self.open.top().key[1]

            # 4.3) extraer nodo de focal y quitar de open
            node = self.preferred.extract()
            self.open.extract(node.heap_index[0])
            self.expansions += 1

            # 4.4) si es meta, reconstruir camino y salir
            if node.state.is_goal():
                elapsed = (time.time() - t0) * 1000
                return SearchResult(node.path(), self.expansions, elapsed)

            # 4.5) obtener política (vector de 4) en node
            policy = self.inad_h(node.state)
            best_a = np.argmax(policy)

            # 4.6) expandir sucesores clásicos
            for child_state, action, cost, _ in node.state.h_successors(self.inad_h):
                g2 = node.g + cost
                child = self.generated.get(child_state)

                # 4.6.1) Si es nuevo o encontramos un camino más corto
                if child is None or g2 < child.g:
                    if child is None:
                        child = MultiNode(child_state)
                        self.generated[child_state] = child

                    child.parent = node
                    child.action = action
                    child.g      = g2

                    # 4.6.2) heurística admisible
                    child.h[0] = self.adm_h(child_state)

                    # 4.6.3) calcular discrepancia vs acción recomendada
                    a_idx = node.state.action_to_index(action)
                    delta = 0 if a_idx == best_a else 1
                    child.key[0] = node.key[0] + delta

                    # 4.6.4) actualizar f_adm para open & rango focal
                    child.key[1] = self.fvalue(child.g, child.h[0])

                    # 3.6.5) insertar/reordenar en open
                    self.open.insert(child)
                    # 3.6.6) si cabe en rango focal, insertarlo
                    if child.key[1] <= focal_w * f_min:
                        self.preferred.insert(child)

        # 4) sin solución
        elapsed = (time.time() - t0) * 1000
        return SearchResult([], self.expansions, elapsed)