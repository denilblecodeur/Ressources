#Edmonds-Karp Maximum flow - O(V * E^2)

# + fonctionne si arcs bidirectionnels à capacité partagée

def edmonds_karp(graph, capacity, source, target):
    
    def augment(graph, capacity, flow, source, target):
        n = len(graph)
        A = [0] * n             # A[v] = cap.res.min sur chemin source-v
        augm_path = [None] * n
        Q = deque([source])
        augm_path[source] = source
        A[source] = 1<<59
        while Q:
            u = Q.popleft()
            for v in graph[u]:
                cuv = capacity[u][v]
                residual = cuv - flow[u][v]
                if residual > 0 and augm_path[v] is None:
                    augm_path[v] = u
                    A[v] = min(A[u], residual)
                    if v == target:
                        break
                    else:
                        Q.append(v)
        return augm_path, A[target]       # chemin augmentant, cap.res.min

    # Capacités doivent être entières
    # capacity matrice, si arc (u -> v) existe, (v -> u) doit exister (capa 0)
    add_reverse_arcs(graph, capacity)
    n = len(graph)
    flow = [[0] * n for _ in range(n)]
    while True:
        augm_path, delta = augment(graph, capacity, flow, source, target)
        if delta == 0:
            break
        v = target
        while v != source:
            u = augm_path[v]
            flow[u][v] += delta
            flow[v][u] -= delta
            v = u
    return flow, sum(flow[source])    # flot, valeur du flot