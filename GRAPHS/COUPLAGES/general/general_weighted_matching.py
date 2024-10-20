"""
Given a simple undirected graph with N vertices and M edges. 
i-th edge is (ui, vi) with a weight wi.

Calculate the matching in which the sum of weights is maximized.
N < 500
M < N(N-1)/2
https://judge.yosupo.jp/problem/general_weighted_matching
"""

from collections import deque
INF = 1 << 59

class GeneralWeightedMatching():
    def __init__(self, n):
        self.n = n
        self.nx = n
        self.m = 2 * n + 1
        self.u = [0] * self.m * self.m
        self.v = [0] * self.m * self.m
        self.w = [0] * self.m * self.m
        self.match = [0] * self.m
        self.slack = [0] * self.m
        self.flower = [[] for _ in range(self.m)]
        self.flower_from = [0] * self.m * self.m
        self.label = [0] * self.m
        self.root = [0] * self.m
        self.par = [0] * self.m
        self.col = [0] * self.m
        self.vis = [0] * self.m
        self.que = deque()
        self.t = 0
        for u in range(1, self.m):
            for v in range(1, self.m):
                self.u[u * self.m + v] = u
                self.v[u * self.m + v] = v

    def dist(self, u, v):
        u, v = self.u[u * self.m + v], self.v[u * self.m + v]
        return self.label[u] + self.label[v] - self.w[u * self.m + v] * 2

    def add_edge(self, u, v, w):
        u += 1; v += 1
        self.w[u * self.m + v] = max(self.w[u * self.m + v], w)
        self.w[v * self.m + u] = max(self.w[v * self.m + u], w)

    def update_slack(self, u, x):
        if not self.slack[x] or self.dist(u, x) < self.dist(self.slack[x], x):
            self.slack[x] = u

    def set_slack(self, x):
        self.slack[x] = 0
        for u in range(1, self.n + 1):
            if self.w[u * self.m + x] > 0 and self.root[u] != x and self.col[self.root[u]] == 0:
                self.update_slack(u, x)

    def que_push(self, x):
        stack = [x]
        while stack:
            x = stack.pop()
            if x <= self.n:
                self.que.append(x)
                continue
            for i, fi in enumerate(self.flower[x]):
                stack.append(fi)

    def set_root(self, x, b):
        stack = [x]
        while stack:
            x = stack.pop()
            self.root[x] = b
            if x <= self.n: 
                continue
            for i, fi in enumerate(self.flower[x]):
                stack.append(fi)

    def get_pr(self, b, xr):
        f = self.flower[b]
        pr = f.index(xr)
        if pr % 2 == 1:
            f = self.flower[b] = f[0:1] + f[1:][::-1]
            return len(f) - pr
        else:
            return pr

    def set_match(self, u, v):
        self.match[u] = self.v[u * self.m + v]
        if u <= self.n:
            return
        xr = self.flower_from[u * self.m + self.u[u * self.m + v]]
        pr = self.get_pr(u, xr)
        f = self.flower[u]
        for i in range(pr):
            self.set_match(f[i], f[i ^ 1])
        self.set_match(xr, v)
        self.flower[u] = f[pr:] + f[:pr]

    def augment(self, u, v):
        xnv = self.root[self.match[u]]
        self.set_match(u, v)
        while xnv:
            self.set_match(xnv, self.root[self.par[xnv]])
            u, v = self.root[self.par[xnv]], xnv
            xnv = self.root[self.match[u]]
            self.set_match(u, v)

    def get_lca(self, u, v):
        self.t += 1
        while u or v:
            if not u:
                u, v = v, u
                continue
            if self.vis[u] == self.t:
                return u
            self.vis[u] = self.t
            u = self.root[self.match[u]]
            if u: u = self.root[self.par[u]]
            u, v = v, u
        return 0

    def add_blossom(self, u, lca, v):
        b = self.n + 1
        while b <= self.nx and self.root[b]:
            b += 1
        if b > self.nx:
            self.nx += 1
        self.label[b] = 0
        self.col[b] = 0
        self.match[b] = self.match[lca]
        f = self.flower[b] = []
        f.append(lca)
        x = u
        while x != lca:
            f.append(x)
            y = self.root[self.match[x]]
            f.append(y)
            self.que_push(y)
            x = self.root[self.par[y]]
        f = self.flower[b] = f[0:1] + f[1:][::-1]
        x = v
        while x != lca:
            f.append(x)
            y = self.root[self.match[x]]
            f.append(y)
            self.que_push(y)
            x = self.root[self.par[y]]
        self.set_root(b, b)
        for x in range(1, self.nx + 1):
            self.w[b * self.m + x] = self.w[x * self.m + b] = 0
        for x in range(1, self.n + 1):
            self.flower_from[b * self.m + x] = 0
        for i, xs in enumerate(f):
            for x in range(1, self.nx + 1):
                if self.w[b * self.m + x] == 0 or self.dist(xs, x) < self.dist(b, x):
                    self.u[b * self.m + x] = self.u[xs * self.m + x]
                    self.u[x * self.m + b] = self.u[x * self.m + xs]
                    self.v[b * self.m + x] = self.v[xs * self.m + x]
                    self.v[x * self.m + b] = self.v[x * self.m + xs]
                    self.w[b * self.m + x] = self.w[xs * self.m + x]
                    self.w[x * self.m + b] = self.w[x * self.m + xs]
            for x in range(1, self.n + 1):
                if self.flower_from[xs * self.m + x]:
                    self.flower_from[b * self.m + x] = xs
        self.set_slack(b)

    def expand_blossom(self, b):
        f = self.flower[b]
        for i, fi in enumerate(f):
            self.set_root(fi, fi)
        xr = self.flower_from[b * self.m + self.u[b * self.m + self.par[b]]]
        pr = self.get_pr(b, xr)
        f = self.flower[b]
        for i in range(0, pr, 2):
            xs = f[i]
            xns = f[i + 1]
            self.par[xs] = self.u[xns * self.m + xs]
            self.col[xs] = 1
            self.col[xns] = 0
            self.slack[xs] = 0
            self.set_slack(xns)
            self.que_push(xns)
        self.col[xr] = 1
        self.par[xr] = self.par[b]
        for i in range(pr + 1, len(f)):
            xs = f[i]
            self.col[xs] = -1
            self.set_slack(xs)
        self.root[b] = 0

    def on_found_edge(self, u, v):
        eu = self.u[u * self.m + v]
        ev = self.v[u * self.m + v]
        u = self.root[eu]
        v = self.root[ev]
        if self.col[v] == -1:
            self.par[v] = eu
            self.col[v] = 1
            nu = self.root[self.match[v]]
            self.slack[v] = self.slack[nu] = 0
            self.col[nu] = 0
            self.que_push(nu)
        elif self.col[v] == 0:
            lca = self.get_lca(u, v)
            if not lca:
                self.augment(u, v)
                self.augment(v, u)
                return 1
            else:
                self.add_blossom(u, lca, v)
        return 0

    def matching(self):
        for i in range(self.nx + 1):
            self.col[i] = -1
            self.slack[i] = 0
        self.que.clear()
        for x in range(1, self.nx + 1):
            if self.root[x] == x and not self.match[x]:
                self.par[x] = 0
                self.col[x] = 0
                self.que_push(x)
        if not self.que:
            return 0
        while True:
            while self.que:
                u = self.que.popleft()
                if self.col[self.root[u]] == 1:
                    continue
                for v in range(1, self.n + 1):
                    if self.w[u * self.m + v] and self.root[u] != self.root[v]:
                        if self.dist(u, v) == 0:
                            if self.on_found_edge(u, v):
                                return 1
                        else:
                            self.update_slack(u, self.root[v])
            d = INF
            for b in range(self.n + 1, self.nx + 1):
                if self.root[b] == b and self.col[b] == 1:
                    d = min(d, self.label[b] // 2)
            for x in range(1, self.nx + 1):
                if self.root[x] == x and self.slack[x]:
                    if self.col[x] == -1:
                        d = min(d, self.dist(self.slack[x], x))
                    elif self.col[x] == 0:
                        d = min(d, self.dist(self.slack[x], x) // 2)
            for u in range(1, self.n + 1):
                if self.col[self.root[u]] == 0:
                    if self.label[u] <= d:
                        return 0
                    self.label[u] -= d
                elif self.col[self.root[u]] == 1:
                    self.label[u] += d
            for b in range(self.n + 1, self.nx + 1):
                if self.root[b] == b:
                    if self.col[b] == 0:
                        self.label[b] += d * 2
                    elif self.col[b] == 1:
                        self.label[b] -= d * 2
            self.que.clear()
            for x in range(1, self.nx + 1):
                if self.root[x] == x and self.slack[x] and self.root[self.slack[x]] != x and self.dist(self.slack[x], x) == 0:
                    if self.on_found_edge(self.slack[x], x):
                        return 1
            for b in range(self.n + 1, self.nx + 1):
                if self.root[b] == b and self.col[b] == 1 and self.label[b] == 0:
                    self.expand_blossom(b)
        return 0

    def solve(self):
        cnt = 0
        ans = 0
        for u in range(self.n + 1):
            self.root[u] = u
            self.flower[u].clear()
        w_max = 0
        for u in range(1, self.n + 1):
            for v in range(1, self.n + 1):
                self.flower_from[u * self.m + v] = u if u == v else 0
                w_max = max(w_max, self.w[u * self.m + v])
        for u in range(1, self.n + 1):
            self.label[u] = w_max
        while self.matching():
            cnt += 1
        for u in range(1, self.n + 1):
            if self.match[u] and self.match[u] < u:
                ans += self.w[u * self.m + self.match[u]]
        for i in range(self.n):
            self.match[i] = self.match[i + 1] - 1
        return ans, cnt

N, M = map(int, input().split())
G = GeneralWeightedMatching(N)

for _ in range(M):
    u, v, w = map(int, input().split())
    G.add_edge(u, v, w)

W, X = G.solve()
print(X, W)

for i in range(N):
    if G.match[i] > i:
        print(i, G.match[i])