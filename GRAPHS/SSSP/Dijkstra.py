# DIJKSTRA LIMIT

def dijkstra(src, dest, graph, limit):
    heap = [(0, 0, src)]
    distances = {src: {0: 0}}
    while heap:
        current_cost, current_dist, node = heappop(heap)
        if node == dest:
            return current_cost
        for cost_n, dist_n, neigh in graph[node]:
            newdist = current_dist + dist_n
            newcost = current_cost + cost_n
            if newdist <= limit:
                if neigh not in distances:
                    distances[neigh] = {}
                if newdist not in distances[neigh] or distances[neigh][newdist] > newcost:
                    distances[neigh][newdist] = newcost 
                    heappush(heap, (newcost, newdist, neigh))
    return -1

# DIJKSTRA DENSE GRAPH
prev = [[i] * n for i in range(n)]
for i in range(n):
    dist[i][i] = adj_mat[i][i] = 0
for k in range(n):
    for i in range(n):
        for j in range(n):
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
                prev[i][j] = prev[k][j]

def dijkstra(s, t):
    d = [1<<59] * n
    d[s] = 0
    vis = [False] * n
    for _ in range(n):
        v = -1
        for j in range(n):
            if not vis[j] and (v == -1 or d[j] < d[v]):
                v = j
        if d[v] == 1<<59:
            break
        vis[v] = True
        for u in adj_list[v]:
            if (v==s and u==t) or (v==t and u==s):
                continue
            #if d[v]+adj_mat[v][u] < d[u]:
            #   d[u] = d[v]+adj_mat[v][u]
            if prev[u][t] != s:
                d[t] = min(d[t], d[v] + adj_mat[v][u] + dist[u][t])
            else:
                d[u] = min(d[u], d[v] + adj_mat[v][u])
    return d[t] if d[t] != 1<<59 else -1