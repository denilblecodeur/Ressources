# Dilworth’s theorem states
# that in a directed acyclic graph, the size of a minimum general path cover equals
# the size of a maximum antichain.
# https://usaco.guide/CPH.pdf#page=200

# Largeur d'un ordre partiel = taille de la plus grande anti-chaîne
# Retourne partition en chaînes

def dilworth(graph):
    """
    Produire un graphe biparti H(V-, V+, E) avec V-, V+ étant des copies de V,
    et (u-, v+) appartient à E ssi (u, v) appartient à A
    """
    n = len(graph)
    #match = max_bipartite_matching(graph)   # couplage maximum
    match = [None] * n
    for a, b in bm.solve():
        match[b] = a
    part = [None] * n                       # partition en chaînes
    nb_chains = 0
    for v in range(n - 1, -1, -1):          # dans l'ordre topologique inverse
        if part[v] is None:                 # début d'une chaîne
            u = v
            while u is not None:            # suivre la chaîne
                part[u] = nb_chains         # marquer
                u = match[u]
            nb_chains += 1
    return part