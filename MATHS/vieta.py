"""
Quel que soit le degré n d'un polynôme,
et quelle que soit la nature de ses racines (réelles ou complexes),
on aura toujours :

(- b / a) = somme de toutes les racines
(-1) ^ n * (k / a) = produit de toutes les racines

où k est le coeff du monome de degré 0, a degré n, b degré n - 1
"""

# Vieta's formula for quadratic equations
# given x, y, find the number of pairs i and j (0 <= i < j < n) that both ai + aj = x and ai * aj = y
from collections import Counter

n = int(input())
a = list(map(int,input().split()))
c = Counter(map(str,a))
ans = []
for _ in range(int(input())):
    x, y = map(int,input().split())
    delta = x**2 - 4 * y
    if delta < 0:
        ans.append(0)
        continue
    delta = int(delta**.5)
    if delta == 0:
        if x % 2:
            ans.append(0)
        else:
            ans.append((c.get(str(x // 2), 0) * (c.get(str(x // 2), 0) - 1)) // 2)
    else:
        X1 = (x + delta) // 2
        X2 = (x - delta) // 2
        if X1 + X2 != x or X1 * X2 != y:
            ans.append(0)
        else:
            ans.append(c.get(str(X1), 0) * c.get(str(X2), 0))