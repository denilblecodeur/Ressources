import sys
input = sys.stdin.buffer.readline


from collections import deque

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
    return flow, total

def add_edge(u, v, c):
    if v not in graph[u]:
        graph[u][v] = graph[v][u] = 0
    graph[u][v] = c

n, m, k = map(int,input().split())
source, target = 0, n+k+m+1
SOURCE, TARGET = target+1, target+2
graph = [{} for _ in range(TARGET+1)]
sing = lambda v:v       # 1 -> n
lang = lambda v:n+v     # n+1 -> n+k
song = lambda v:n+k+v   # n+k+v
for _ in range(k):
    p, s, l = map(int,input().split())
    add_edge(sing(p), lang(l), 1)
    add_edge(lang(l), song(s), 1)
for p in range(1, n+1):
    add_edge(source, sing(p), 1<<59)
    add_edge(SOURCE, sing(p), 1)
for s in range(1, m+1):
    add_edge(song(s), target, 1<<59)
    add_edge(song(s), TARGET, 1)
add_edge(SOURCE, target, m)
add_edge(source, TARGET, n)
add_edge(target, source, 1<<59)
flow, mf = dinic(SOURCE, TARGET, graph)
print(mf, mf == min(m+1, n+1))

