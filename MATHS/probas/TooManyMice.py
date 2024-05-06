mois = int(input("entrer nombre de mois : "))
portee = int(input("entrer nombre de bébés par portée : "))
maturite = int(input("entrer délai en mois avant maturité : "))

assert maturite>1, "délai maturité doit être > 1"

# BRUTEFORCE en O(mois * maturite)
stade = [1] + [0] * maturite
for _ in range(mois):
    stade[-1] += stade[-2]
    for j in range(maturite-2, -1, -1): stade[j+1] = stade[j]
    stade[0] = portee * stade[-1]
print(sum(stade))

# FORMULE en O(mois ^ 2)
import math
print(
    1
    +
    sum(
        portee**i * math.comb(mois-j, i)
        for i, j in enumerate(range(maturite-1, mois + 1, maturite-1), 1)
        )
)