"""
Given a simple undirected graph with N vertices and M edges. 
i-th edge is (ui, vi)
Calculate the maximum matching.

N < 500
M < N(N-1)/2
https://judge.yosupo.jp/problem/general_matching
"""

from collections import deque

class GeneralMatching:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n + 1)]
        self.edges = []
        self.cnt = n + 1
        self.mate = [0] * (n + 1)
        self.label = [-1] * (n + 1)
        self.first = [0] * (n + 1)

    def add_edge(self, u, v): #0-indexed
        self.graph[u + 1].append((v + 1, self.cnt))
        self.graph[v + 1].append((u + 1, self.cnt))
        self.edges.append((u + 1, v + 1))
        self.cnt += 1

    def eval_first(self, x):
        if self.label[self.first[x]] < 0:
            return self.first[x]
        self.first[x] = self.eval_first(self.first[x])
        return self.first[x]

    def rematch(self, u, v):
        t = self.mate[u]
        self.mate[u] = v
        if self.mate[t] != u: return
        if self.label[u] <= self.n:
            self.mate[t] = self.label[u]
            self.rematch(self.label[u], t)
        else:
            x, y = self.edges[self.label[u] - self.n - 1]
            self.rematch(x, y)
            self.rematch(y, x)

    def assign(self, x, y, num):
        r = self.eval_first(x)
        s = self.eval_first(y)
        join = 0
        if r == s: return
        self.label[r] = -num
        self.label[s] = -num
        while True:
            if s != 0: r, s = s, r
            r = self.eval_first(self.label[self.mate[r]])
            if self.label[r] == -num:
                join = r
                break
            self.label[r] = -num
        v = self.first[x]
        while v != join:
            self.queue.append(v)
            self.label[v] = num
            self.first[v] = join
            v = self.first[self.label[self.mate[v]]]
        v = self.first[y]
        while v != join:
            self.queue.append(v)
            self.label[v] = num
            self.first[v] = join
            v = self.first[self.label[self.mate[v]]]
        return

    def check(self, v):
        self.first[v] = 0
        self.label[v] = 0
        self.queue.append(v)
        while self.queue:
            x = self.queue.popleft()
            for y, lb in self.graph[x]:
                if self.mate[y] == 0 and y != v:
                    self.mate[y] = x
                    self.rematch(x, y)
                    return True
                elif self.label[y] >= 0:
                    self.assign(x, y, lb)
                elif self.label[self.mate[y]] < 0:
                    self.label[self.mate[y]] = x
                    self.first[self.mate[y]] = y
                    self.queue.append(self.mate[y])
        return False

    def solve(self):
        for i in range(1, self.n + 1):
            self.queue = deque()
            if self.mate[i] != 0: continue
            if self.check(i):
                self.label = [-1] * (self.n + 1)
        res = []
        for i in range(1, self.n + 1):
            if i < self.mate[i]:
                res.append((i - 1, self.mate[i] - 1))
        return res

N, M = map(int, input().split())

g = GeneralMatching(N)

for _ in range(M):
    u, v = map(int, input().split())
    g.add_edge(u, v)

res = g.solve()

print(len(res))

for u, v in res:
    print(u, v)