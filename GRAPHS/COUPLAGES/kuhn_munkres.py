"""Couplage parfait de profit maximal en O(|U|^2 * |V|)
 - si minimal, changer signe des poids
 - si |U| > |V|, ajouter sommets à V reliés à
   tous les sommets de U par un poids 0
 - si graph non complet, le compléter avec arêtes
   de poids -inf
"""

def kuhn_munkres(G, TOLERANCE=1e-6):
    """
    G: weight matrix where G[u][v] is the weight of edge (u,v),
    TOLERANCE: If G consists of integer or fractional values
               then TOLERANCE can be chosen 0.
    graph (U,V,E) is complete bi-partite graph with len(U) <= len(V)
        float('-inf') or float('inf') entries in G are allowed.
    returns matching table from U to V, value of matching
    """
    assert len(G) <= len(G[0])
    nU, nV = len(G), len(G[0])
    U, V = range(nU), range(nV)
    mu = [None] * nU                # empty matching
    mv = [None] * nV
    lu = [max(row) for row in G]    # trivial labels
    lv = [0] * nV
    for root in U:                  # build an alternate tree
        au = [False] * nU           # au, av mark nodes...
        au[root] = True             # ... covered by the tree
        Av = [None] * nV            # Av[v] successor of v in the tree
        # for every vertex u, slack[u] := (val, v) such that
        # val is the smallest slack on the constraints (*)
        # with fixed u and v being the corresponding vertex
        slack = [(lu[root] + lv[v] - G[root][v], root) for v in V]
        while True:
            (delta, u), v = min((slack[v], v) for v in V if Av[v] is None)
            assert au[u]
            if delta > TOLERANCE:   # tree is full
                for u0 in U:        # improve labels
                    if au[u0]:
                        lu[u0] -= delta
                for v0 in V:
                    if Av[v0] is not None:
                        lv[v0] += delta
                    else:
                        (val, arg) = slack[v0]
                        slack[v0] = (val - delta, arg)
            assert abs(lu[u] + lv[v] - G[u][v]) <= TOLERANCE  # equality
            Av[v] = u                # add (u, v) to A
            if mv[v] is None:
                break                # alternating path found
            u1 = mv[v]
            assert not au[u1]
            au[u1] = True            # add (u1, v) to A
            for v1 in V:
                if Av[v1] is None:   # update margins
                    alt = (lu[u1] + lv[v1] - G[u1][v1], u1)
                    if slack[v1] > alt:
                        slack[v1] = alt
        while v is not None:         # ... alternating path found
            u = Av[v]                # along path to root
            prec = mu[u]
            mv[v] = u                # augment matching
            mu[u] = v
            v = prec
    return (mu, sum(lu) + sum(lv))

"""
La foire aux jeux - Battle Dev RegionsJob Mars 2017
-> Maximiser échanges entre n participants
"""

def kuhn_munkres(G, TOLERANCE = 1e-6):
    assert len(G) == len(G[0])
    n = len(G)
    U = V = range(n)
    mu = [None] * n
    mv = [None] * n
    lu = [max(row) for row in G]
    lv = [0] * n
    for root in U:
        n = len(G)
        au = [False] * n
        au[root] = True
        Av = [None] * n
        marge = [(lu[root] + lv[v] - G[root][v], root) for v in V]
        while True:
            ((delta, u), v) = min((marge[v], v) for v in V if Av[v] == None)
            assert au[u]
            if delta > TOLERANCE:
                for u0 in U:
                    if au[u0]:
                        lu[u0] -= delta
                for v0 in V:
                    if Av[v0] is not None:
                        lv[v0] += delta
                    else:
                        (val, arg) = marge[v0]
                        marge[v0] = (val - delta, arg)
            assert abs(lu[u] + lv[v] - G[u][v]) <= TOLERANCE
            Av[v] = u
            if mv[v] is None:
                break
            u1 = mv[v]
            assert not au[u1]
            au[u1] = True
            for v1 in V:
                if Av[v1] is None:
                    alt = (lu[u1] + lv[v1] - G[u1][v1], u1)
                    if marge[v1] > alt:
                        marge[v1] = alt
        while v is not None:
            u = Av[v]
            prec = mu[u]
            mv[v] = u
            mu[u] = v
            v = prec
    return (mu,  sum(lu) + sum(lv))


n = int(input())
m = int(input())
G = [[float('-inf')] * n for i in range(n)]
for i in range(n):
    G[i][i] = 0
for i in range(m):
    u, v = map(int, input().split())
    G[u - 1][v - 1] = 1
mu, val = kuhn_munkres(G)

for i in range(n):
    if mu[i] == i:
        mu[i] = 0
    else:
        mu[i] += 1

print(' '.join(str(u) for u in mu))


# ALTERNATIVE
# https://judge.yosupo.jp/problem/assignment
# O(n^3)

def hungarian(A):
    inf = 1 << 40
    n = len(A) + 1
    m = len(A[0]) + 1
    P = [0] * m
    way = [0] * m
    U = [0] * n
    V = [0] * n
    for i in range(1, n):
        P[0] = i
        minV = [inf] * m
        used = [False] * m
        j0 = 0
        while P[j0] != 0:
            i0 = P[j0]
            j1 = 0
            used[j0] = True
            delta = inf
            for j in range(1, m):
                if used[j]:
                    continue
                if i0 == 0 or j == 0:
                    cur =  -U[i0] - V[j]
                else:
                    cur = A[i0 - 1][j - 1] - U[i0] - V[j]
                if cur < minV[j]:
                    minV[j] = cur
                    way[j] = j0
                if minV[j] < delta:
                    delta = minV[j]
                    j1 = j
            for j in range(m):
                if used[j]:
                    U[P[j]] += delta
                    V[j] -= delta
                else:
                    minV[j] -= delta
            j0 = j1
        P[j0] = P[way[j0]]
        j0 = way[j0]
        while j0 != 0:
            P[j0] = P[way[j0]]
            j0 = way[j0]
    
    ret = [-1] * (n - 1)
    for i in range(1, m):
        if P[i] != 0:
            ret[P[i] - 1] = i - 1
    return -V[0], ret

n = int(input())
A = [list(map(int, input().split())) for _ in range(n)]
cost, P = hungarian(A)
print(cost)
print(*P)