"""Mariages stables - Gale Shapley en O(n^2)
men et women numérotés de 0 à n - 1
Le tableau men contient pour chaque homme
la liste des femmes par préférence décroissante
Même chose pour women
"""
from collection import deque

def gale_shapley(men, women):
    n = len(men)
    assert n == len(women)
    suiv = [0] * n
    mari = [None] * n
    rank = [[0] * n for j in range(n)]  # build rank
    for j in range(n):
        for r in range(n):
            rank[j][women[j][r]] = r
    singles = deque(range(n))  # all men are single and get in the queue
    while singles:
        i = singles.popleft()
        j = men[i][suiv[i]]
        suiv[i] += 1
        if mari[j] is None:
            mari[j] = i
        elif rank[j][mari[j]] < rank[j][i]:
            singles.append(i)
        else:
            singles.put(mari[j])  # divorce mari[j]
            mari[j] = i
    return mari