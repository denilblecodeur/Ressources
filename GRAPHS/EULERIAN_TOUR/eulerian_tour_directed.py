def eulerian_tour_directed(graph):
    P, Q, R = [], [0], []
    _next = [0] * len(graph)
    while Q:
        node = Q.pop()
        P.append(node)
        while _next[node] < len(graph[node]):
            neigh = graph[node][_next[node]]
            _next[node] += 1
            R.append(neigh)
            node = neigh
        while R:
            Q.append(R.pop())
    return P