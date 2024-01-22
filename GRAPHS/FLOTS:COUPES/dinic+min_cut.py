def mincut(source, target, graph):
    flow, _ = dinic(source, target, graph)
    reachable = set([source])
    Q = [source]
    seen = set()
    while Q:
        u = Q.pop()
        seen.add(u)
        for v in graph[u]:
            if v not in seen and graph[u][v] > flow[u][v]:
                reachable.add(v)
                Q.append(v)
    cut = []
    for u in reachable:
        for v in graph[u]:
            if v not in reachable:
                cut.append((u, v))
    return cut