import sys

for line in sys.stdin.buffer:
    ev1, ev2, at, d = map(int,line.split())
    if ev1 == ev2 == at == d == 0: break
    n1, n2 = (ev1+d-1) // d, (ev2+d-1) // d
    p = at / 6
    if p == 1-p:
        ans = n1 / (n1+n2)
    else:
        q = 1-p
        ans = (1-(q/p)**n1) / (1-(q/p)**(n1+n2))
    print("{:.01f}".format(100 * ans))

"""
https://www.columbia.edu/~ks20/FE-Notes/4700-07-Notes-GR.pdf
Gambler's ruin problem

After each flip of the coin the loser transfers one penny to the winner.
The game ends when one player has all the pennies.

P1 = probability of P1 getting ruined
n1, n2 = nb of pennies of 1, 2
Fair coin flipping:
    P1 = n1 / (n1+n2)
Unfair coin flipping:
    P1 = (1 - pow(p/q, n2)) / (1 - pow(p/q, n1+n2))
"""