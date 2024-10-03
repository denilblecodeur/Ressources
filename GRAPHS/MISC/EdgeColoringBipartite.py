# V<2e5, E<1e5
# https://judge.yosupo.jp/problem/bipartite_edge_coloring

from random import shuffle
from heapq import *



def bipartite_matching(
    n: int, m: int, edges: list[tuple[int, int]]
) -> list[tuple[int, int]]:

    shuffle(edges)

    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)

    prev = [-1] * n
    root = [-1] * n
    p = [-1] * n
    q = [-1] * m
    updated = True
    while updated:
        updated = False
        s = []
        for v in range(n):
            if p[v] == -1:
                root[v] = v
                s.append(v)
        i = 0
        while i < len(s):
            v = s[i]
            i += 1
            if p[root[v]] != -1:
                continue
            for u in adj[v]:
                if q[u] == -1:
                    while u != -1:
                        q[u] = v
                        p[v], u = u, p[v]
                        v = prev[v]
                    updated = True
                    break
                u = q[u]
                if prev[u] != -1:
                    continue
                prev[u] = v
                root[u] = root[v]
                s.append(u)
        if updated:
            for v in range(n):
                prev[v] = -1
                root[v] = -1
    return p, q

class UnionFind:
    def __init__(self, n: int):
        self.n = n
        self.parent_or_size = [-1 for i in range(n)]

    def merge(self, a: int, b: int) -> int:
        # assert 0 <= a < self.n, "0<=a<n,a={0},n={1}".format(a, self.n)
        # assert 0 <= b < self.n, "0<=b<n,b={0},n={1}".format(b, self.n)
        x = self.leader(a)
        y = self.leader(b)
        if x == y:
            return x
        if -self.parent_or_size[x] < -self.parent_or_size[y]:
            x, y = y, x
        self.parent_or_size[x] += self.parent_or_size[y]
        self.parent_or_size[y] = x
        return x

    def same(self, a: int, b: int) -> bool:
        # assert 0 <= a < self.n, "0<=a<n,a={0},n={1}".format(a, self.n)
        # assert 0 <= b < self.n, "0<=b<n,b={0},n={1}".format(b, self.n)
        return self.leader(a) == self.leader(b)

    def leader(self, a: int) -> int:
        # assert 0 <= a < self.n, "0<=a<n,a={0},n={1}".format(a, self.n)
        if self.parent_or_size[a] < 0:
            return a
        self.parent_or_size[a] = self.leader(self.parent_or_size[a])
        return self.parent_or_size[a]

    def size(self, a: int) -> int:
        # assert 0 <= a < self.n, "0<=a<n,a={0},n={1}".format(a, self.n)
        return -self.parent_or_size[self.leader(a)]

    def groups(self) -> list[int]:
        leader_buf = [0 for i in range(self.n)]
        for i in range(self.n):
            leader_buf[i] = self.leader(i)
        result = [[] for _ in range(self.n)]
        for i in range(self.n):
            result[leader_buf[i]].append(i)
        return [group for group in result if len(group) > 0]




class RegularBipartiteGlaph:
    def __init__(self, l: int, r: int, edges: list[tuple[int, int]]):
        self.l = l
        self.r = r
        self.el = []
        self.er = []
        for u, v in edges:
            self.el.append(u)
            self.er.append(v)
        self._regularize()

    def _contract(self, deg: list[int], k: int) -> UnionFind:
        pq = [(d, i) for i, d in enumerate(deg)]
        heapify(pq)
        uf = UnionFind(len(deg))
        while len(pq) > 1:
            di, i = heappop(pq)
            dj, j = heappop(pq)
            if di + dj > k:
                continue
            i = uf.merge(i, j)
            heappush(pq, (di + dj, i))
        return uf

    def _regularize(self):
        dl = [0] * self.l
        dr = [0] * self.r
        for i in self.el:
            dl[i] += 1
        for i in self.er:
            dr[i] += 1
        self.k = k = max(max(dl), max(dr))
        ufl = self._contract(dl, k)
        ufr = self._contract(dr, k)
        cl = cr = 0
        idl = [0] * self.l
        idr = [0] * self.r
        for i in range(self.l):
            if ufl.leader(i) == i:
                idl[i] = cl
                cl += 1
        for i in range(self.r):
            if ufr.leader(i) == i:
                idr[i] = cr
                cr += 1
        self.n = n = max(cl, cr)
        self.lt = []
        self.rt = []
        dl = [0] * n
        dr = [0] * n
        for i in range(len(self.el)):
            l = idl[ufl.leader(self.el[i])]
            r = idr[ufr.leader(self.er[i])]
            self.lt.append(l)
            self.rt.append(r)
            dl[l] += 1
            dr[r] += 1
        j = 0
        for i in range(n):
            while dl[i] < k:
                while dr[j] == k:
                    j += 1
                self.lt.append(i)
                self.rt.append(j)
                dl[i] += 1
                dr[j] += 1


class BipartiteEdgeColoring:
    def __init__(self, rg: RegularBipartiteGlaph):
        self.n = rg.n
        self.k = rg.k
        self.lt = rg.lt
        self.rt = rg.rt
        self.group = []
        self.color = [-1] * self.n * self.k

    def euler_trail(self, eis: list[int]) -> list[tuple[int, int]]:
        g = [[] for _ in range(self.n * 2)]
        m = len(eis)
        for i, ei in enumerate(eis):
            g[self.lt[ei]].append((self.rt[ei] + self.n, i))
            g[self.rt[ei] + self.n].append((self.lt[ei], i))
        used_vtx = [False] * self.n * 2
        used_edge = [False] * m
        res = []
        for i in range(2 * self.n):
            if used_vtx[i]:
                continue
            st = [(i, -1)]
            ord = []
            while st:
                j = st[-1][0]
                used_vtx[j] = True
                if g[j]:
                    v, ei = g[j].pop()
                    if used_edge[ei]:
                        continue
                    used_edge[ei] = True
                    st.append((v, ei))
                else:
                    v, ei = st.pop()
                    ord.append(ei)
            res.extend(ord[:-1][::-1])
        for i, p in enumerate(res):
            res[i] = eis[p]
        return res

    def solve(self):
        ord = list(range(len(self.lt)))
        st = [(self.k, ord)]
        while st:
            k, eis = st.pop()
            if k == 0:
                continue
            if k == 1:
                self.group.append(eis)
            elif k & 1 == 0:
                path = self.euler_trail(eis)
                ord1 = []
                ord2 = []
                for i, p in enumerate(path):
                    if i & 1 == 0:
                        ord1.append(p)
                    else:
                        ord2.append(p)
                st += [(k // 2, ord1), (k // 2, ord2)]
            else:
                match_l, _ = bipartite_matching(
                    self.n, self.n, [(self.lt[ei], self.rt[ei]) for ei in eis]
                )
                ord = []
                matched = []
                for ei in eis:
                    if match_l[self.lt[ei]] == self.rt[ei]:
                        match_l[self.lt[ei]] = -1
                        matched.append(ei)
                    else:
                        ord.append(ei)
                self.group.append(matched)
                st.append((k - 1, ord))
        for i in range(self.k):
            for j in self.group[i]:
                self.color[j] = i



l, r, m = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]
rg = RegularBipartiteGlaph(l, r, edges)
bec = BipartiteEdgeColoring(rg)
bec.solve()

print(rg.k)
print(*bec.color[:m], sep="\n")