#Problème de couplage maximal
#Problème de couverture minimale

# Small instances ~10^3 ####################################
def max_bipartite_matching(bigraph, n, m):
    def augment(u):
        if visit[u]:
            return False
        visit[u] = True
        for v in bigraph[u]:
            if matching[v] == -1 or augment(matching[v]):
                matching[v] = u
                return True
        return False
    matching = [-1] * (n + m)
    for u in range(n):
        visit = [False] * n
        augment(u)
    return matching

# Big instances ~10^5 ######################################
class BipartiteMatching:
    def __init__(self, n, m):
        self._n = n
        self._m = m
        self._to = [[] for _ in range(n)]

    def add_edge(self, a, b):
        self._to[a].append(b)

    def solve(self):
        n, m, to = self._n, self._m, self._to
        prev = [-1] * n
        root = [-1] * n
        p = [-1] * n
        q = [-1] * m
        updated = True
        while updated:
            updated = False
            s = []
            s_front = 0
            for i in range(n):
                if p[i] == -1:
                    root[i] = i
                    s.append(i)
            while s_front < len(s):
                v = s[s_front]
                s_front += 1
                if p[root[v]] != -1:
                    continue
                for u in to[v]:
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
                for i in range(n):
                    prev[i] = -1
                    root[i] = -1
        return [(v, p[v]) for v in range(n) if p[v] != -1]

n, m, k = map(int, input().split())
bm = BipartiteMatching(n, m)
for _ in range(k):
    a, b = map(int, input().split())
    bm.add_edge(a - 1, b - 1)
ans = bm.solve()
print(len(ans))
for a, b in ans:
    print(a + 1, b + 1)