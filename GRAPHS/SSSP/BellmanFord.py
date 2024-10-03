def bellman_ford(graph, weight, source=0):
    n = len(graph)
    dist = [INF] * n
    dist[source] = 0
    prec = [None] * n
    for _ in range(n + 2):
        changed = False
        for node in range(n):
            for neigh in graph[node]:
                alt = dist[node] + weight[node][neigh]
                if alt < dist[neigh]:
                    dist[neigh] = alt
                    prec[neigh] = node
                    changed = True
        if not changed:
            return dist, prec, False
    return dist, prec, True

#fast!!
def bellman_ford(edges): # 1 indexed
    dist = [INF] * (n + 1)
    prec = [-1] * (n + 1)

    for _ in range(n):
        x = -1
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                prec[v] = u
                dist[v] = dist[u] + w
                x = v
    if x != -1:
        for _ in range(n):
            x = prec[x]
        end = x
        path = [x]
        while prec[x] != end:
            x = prec[x]
            path.append(x)
        path.append(end)
        return path[::-1]
    return []

#detect neg cycle
# High Score - add neg weight to edges so yield max value obtainable
D = [INF] * n
D[0] = 0
for _ in range(n):
    for node, neigh, weight in edges:
        D[neigh] = min(D[neigh], D[node] + weight)
for _ in range(n):
    for node, neigh, weight in edges:
        if D[node] + weight < D[neigh]:
            D[neigh] = - INF
max_length = - D[n - 1]