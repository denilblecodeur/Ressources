# Flot de K unités de coût minimal (K = INF si flot maximal recherché)
# 0 <= n <= 100, 0 <= m <= 1000, capa_max < 10^9
# flots bloquants binaires (?) n * m * log(capa_max)

# src = https://judge.yosupo.jp/submission/26494

# Comment l'adapter à https://open.kattis.com/problems/mincostmaxflow ?

from heapq import heappop, heappush
INF = 1 << 60

class MinCostFlow:
    def __init__(self, n):
        self.n = n
        self.edges = []
        self._E = [[] for _ in range(n + 1)]
        self._b = [0] * (n + 1)
        self._u = 1

    def add_supply(self, v, amount):
        self.add_edge(self.n, v, amount, amount, 0, False)

    def add_edge(self, u, v, lower, upper, cost, append = True):
        e = [v, upper, cost, 0]
        rev = [u, -lower, -cost, e]
        e[-1] = rev
        self._E[u].append(e)
        self._E[v].append(rev)
        self._u = max(self._u, upper - lower)
        if not lower <= 0 <= upper:
            self._push(e, lower)
        if append:
            self.edges.append((e, upper))

    def _push(self, e, f):
        rev = e[-1]
        self._b[rev[0]] -= f
        self._b[e[0]] += f
        e[1] -= f
        rev[1] += f

    def _saturate(self, delta):
        for v in range(self.n + 1):
            for e in self._E[v]:
                nv, cap, cost, _ = e
                if cap >= delta and cost + self._p[v] - self._p[nv] < 0:
                    self._push(e, cap)

    def _shortest_path(self, delta):
        n = self.n + 1
        dist = [INF] * n
        heap = []
        for v, b in enumerate(self._b):
            if b >= delta:
                dist[v] = 0
                heap.append(v)
        prev = [None] * n
        ward = n.bit_length()
        mask = (1 << ward) - 1
        while heap:
            v = heappop(heap)
            d, v = v >> ward, v & mask
            if dist[v] != d:
                continue
            if self._b[v] <= -delta:
                t = v
                f = -self._b[v]
                while prev[v]:
                    f = min(f, prev[v][1])
                    v = prev[v][-1][0]
                f = min(f, self._b[v])
                while prev[t]:
                    self._push(prev[t], f)
                    t = prev[t][-1][0]
                for v in range(n):
                    self._p[v] += min(d, dist[v])
                return True
            for e in self._E[v]:
                nv, cap, cost, _ = e
                if cap < delta:
                    continue
                if dist[nv] > d + cost + self._p[v] - self._p[nv]:
                    prev[nv] = e
                    dist[nv] = d + cost + self._p[v] - self._p[nv]
                    heappush(heap, dist[nv] << ward | nv)
        return False

    def solve(self):
        self._p = [0] * (self.n + 1)
        delta = 1 << (self._u - 1).bit_length()
        while delta:
            self._saturate(delta)
            while self._shortest_path(delta):
                pass
            delta >>= 1
        return not any(self._b)

# the graph can contain self loops
n, m = map(int, input().split())                  # n vertices, m edges
if not n:
    print(0) & exit()

flow = MinCostFlow(n)
K = int(input())                                  # K = INF if maxflow needed
for v in range(n):
    b = int(input())                              # supply of K for source, -K for sink
    flow.add_supply(v, b)                         # else supply of 0
for _ in range(m):
    u, v, lo, hi, w = map(int, input().split())   # u, v are 0-indexed
    flow.add_edge(u, v, lo, hi, w)                # each edge is directed from vertex u to v,
                                                  # and has a flow lower bound, upper bound, and cost per unit of flow
# to replace with flow.solve() if K == INF
if not flow.solve(): print("infeasible") & exit()

ans = []
f = 0
for e, upper in flow.edges:
    nv, cap, cost, _  = e
    ans.append(upper - cap)
    f += cost * (upper - cap)                    # sum ( used capacity * cost per unit ) for each edge

print(f)                            # sum
print(*flow._p[:-1], sep = '\n')    # "dual p" see (https://judge.yosupo.jp/problem/min_cost_b_flow)
print(*ans, sep = '\n')             # capacity used for each edge