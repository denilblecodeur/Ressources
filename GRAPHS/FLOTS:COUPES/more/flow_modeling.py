# UVa 10779 - Collectors Problem
# https://discuss.codechef.com/t/kgp13h-editorial/4052
# flow modeling : Comment appréhender un problème de flot

import sys
input = sys.stdin.readline
from collections import deque
INF = 1<<60

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

def add_edge(u, v, c):
    if v not in graph[u]:
        graph[u][v] = 0
        graph[v][u] = 0
    graph[u][v] += c

for testcase in range(int(input())):
    n, m = map(int,input().split())
    graph = [{} for _ in range(n + m + 1)]
    source, target = 0, n + m
    stickers = [[0] * m for _ in range(n)]
    for i in range(n):
        line = map(int,input().split())
        next(line)
        for s in line:
            stickers[i][s - 1] += 1
    for i in range(n):
        for s in range(m):
            if i == 0:
                if stickers[0][s] > 0:
                    add_edge(source, s + 1, stickers[0][s])
            else:
                if stickers[i][s] == 0:
                    add_edge(s + 1, m + i, 1)
                elif stickers[i][s] > 1:
                    add_edge(m + i, s + 1, stickers[i][s] - 1)
    for i in range(m):
        add_edge(i + 1, target, 1)
    print("Case #{}: {}".format(testcase + 1, dinic(source, target, graph)))