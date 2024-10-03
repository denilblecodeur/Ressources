dist = [[inf] * n for _ in range(n)]
#init dist
for k in range(n):
    for i in range(n):
        d1 = dist[i][k]
        if k != i and d1 != inf:
            for j in range(i):
                d = d1 + dist[k][j]
                if d < dist[i][j]:
                    dist[i][j] = dist[j][i] = d

def idx(i, j, dim):
    return i + j * dim
def floyd_warshall(n, distances):     
    for k in range(n):
        for i in range(n):
            d1 = distances[idx(i, k, n)]
            if k != i and d1 != INF:
                for j in range(i):
                    t = d1 + distances[idx(k, j, n)]
                    if t < distances[idx(i, j, n)]:
                        distances[idx(i, j, n)] = distances[idx(j, i, n)] = t
    return distances

def floyd_warshall(n, m, edges, dimension):
    D = [INF] * dimension**2
    def idx(i, j):
        return i + j * dimension
    for i in range(n):
        D[idx(i, i)] = 0
    for a, b, c in edges:
        a -= 1; b -= 1
        if c < D[idx(a, b)]:
            D[idx(a, b)] = D[idx(b, a)] = c
    for k in range(n):
        for i in range(n):
            d1 = D[idx(i, k)]
            if k != i and d1 != INF:
                for j in range(i):
                    t = d1 + D[idx(k, j)]
                    if t < D[idx(i, j)]:
                        D[idx(i, j)] = D[idx(j, i)] = t
    return D