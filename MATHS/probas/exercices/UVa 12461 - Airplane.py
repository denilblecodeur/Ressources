import sys

for line in sys.stdin.buffer:
    n = int(line)
    if n == 0: break
    print("1/2")

"""
BRUTEFORCE

def solve(i, n, alloc):
    if i+1 == n:
        return int(alloc.index(False) == i), 1
    if not alloc[i]:
        alloc[i] = True
        return solve(i+1, n, list(alloc))
    good = tot = 0
    for j in range(n):
        if not alloc[j]:
            alloc[j] = True
            g, t = solve(i+1, n, list(alloc))
            good += g
            tot += t
            alloc[j] = False
    return good, tot

n = int(input())
a = [False] * n
good = tot = 0
for j in range(n):
    a[j] = True
    g, t = solve(1, n, list(a))
    good += g
    tot += t
    a[j] = False
print(good / tot)
"""