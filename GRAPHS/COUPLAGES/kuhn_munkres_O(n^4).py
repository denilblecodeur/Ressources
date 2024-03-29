#Couplage parfait de poids maximal
#Problème de couplage parfait dans un graph biparti à profit maximal
#Kuhn-Munkres O(V^3)

def improve_matching(G, u, mu, mv, au, av, lu, lv):
    assert not au[u]
    au[u] = True
    for v in range(len(G)):
        if not av[v] and G[u][v] == lu[u] + lv[v]:
            av[v] = True
            if mv[v] is None or \
            improve_matching(G, mv[v], mu, mv, au, av, lu, lv):
                mv[v] = u
                mu[u] = v
                return True
    return False

def improve_labels(G, au, av, lu, lv):
    U = V = range(len(G))
    delta = min(min(lu[u] + lv[v] - G[u][v]
            for v in V if not av[v]) for u in U if au[u])
    for u in U:
        if au[u]:
            lu[u] -= delta
    for v in V:
        if av[v]:
            lv[v] += delta

def kuhn_munkres(G):                # couplage parfait de profit maximal en O(n^4)
    assert len(G) == len(G[0])
    n = len(G)
    mu = [None] * n                 # couplage vide
    mv = [None] * n
    lu = [max(row) for row in G]    # étiqu. triviaux
    lv = [0] * n
    for u0 in range(n):
        if mu[u0] is None:          # sommet libre
            while True:
                au = [False] * n    # arbre alternant vide
                av = [False] * n
                if improve_matching(G, u0, mu, mv, au, av, lu, lv):
                    break
                improve_labels(G, au, av, lu, lv)
    return (mu, sum(lu) + sum(lv))