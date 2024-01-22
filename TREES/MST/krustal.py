def krustal(graph, weight):
    uf = UnionFind(len(graph))
    edges = []
    for u in range(len(graph)):
        for v in graph[u]:
            edges.append((weight[u][v], u, v))
    edges.sort()
    mst = []
    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v))
    return mst