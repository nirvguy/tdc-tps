class Grafo:
    def __init__(self):
        self.nodos = set()
        self.aristas = dict()

    def agregar_nodo(self, u):
        if u not in self.nodos:
            self.nodos.add(u)

    def lista_aristas(self):
        r = []
        for u, e in self.aristas.items():
            for v, c in e.items():
                r.append((u, v, c))
        return r

    def agregar_arista(self, u, v):
        if u not in self.aristas:
            self.aristas[u] = {}
        self.aristas[u][v] = self.aristas[u].get(v, 0) + 1
