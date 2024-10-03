# UVa 10330 - Power Transmission
import sys
input = sys.stdin.buffer.readline
from collections import deque
INF = 1 << 60

def dinic(source, target, graph):
    def _dinic_step(lev, u, t, limit):
        if limit <= 0: return 0
        if u == t: return limit
        val = 0
        for v in graph[u]:
            residuel = graph[u][v] - flow[u][v]
            if lev[v] == lev[u] + 1 and residuel > 0:
                z = min(limit, residuel)
                aug = _dinic_step(lev, v, t, z)
                flow[u][v] += aug
                flow[v][u] -= aug
                val += aug
                limit -= aug
        if val == 0: lev[u] = None
        return val
    n = len(graph)
    Q = deque()
    total = 0
    flow = [[0] * n for _ in range(n)]
    while True:
        Q.appendleft(source)
        lev = [None] * n
        lev[source] = 0
        while Q:
            u = Q.pop()
            for v in graph[u]:
                if lev[v] is None and graph[u][v] > flow[u][v]:
                    lev[v] = lev[u] + 1
                    Q.appendleft(v)
        if lev[target] is None: break
        UB = sum(graph[source][v] for v in graph[source]) - total
        total += _dinic_step(lev, source, target, UB)
    return total

while True:
    try:
        N = int(input())
        cap = list(map(int,input().split()))
        n = 2 * N + 2
        graph = [{} for _ in range(n)]
        for i, c in enumerate(cap, 1):
            graph[2 * i][2 * i + 1] = c
            graph[2 * i + 1][2 * i] = 0
        M = int(input())
        for _ in range(M):
            i, j, C = map(int,input().split()) # i -> j
            ei, si = 2 * i, 2 * i + 1
            ej, sj = 2 * j, 2 * j + 1
            if ei not in graph[sj]:
                graph[sj][ei] = 0
                graph[ei][sj] = 0
            if ej not in graph[si]:
                graph[si][ej] = 0
                graph[ej][si] = 0
            graph[si][ej] += C
        B, D = map(int,input().split())
        regulator = list(map(int,input().split()))
        for i, r in enumerate(regulator):
            if i < B:
                graph[0][2 * r] = INF
                graph[2 * r][0] = 0
            else:
                graph[2 * r + 1][1] = INF
                graph[1][2 * r + 1] = 0
        print(dinic(0, 1, graph))
    except:break