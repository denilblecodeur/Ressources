def prim(graph):
    visited = [False] * n
    distmin = [float('inf')] * n
    heap = [(0, 0)]
    total = 0
    while heap:
        d, i = heappop(heap)
        if visited[i]:
            continue
        visited[i] = True
        total += d
        for j, w in graph[i]:
            if visited[j]:
                continue
            if d + w < distmin[j]:
                distmin[j] = d + w
                heappush(heap, (d + w, j))
    return total