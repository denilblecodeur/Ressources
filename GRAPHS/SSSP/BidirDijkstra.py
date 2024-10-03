from heapq import *
inf = 1<<20

n = int(input())
grid = [input() for _ in range(n)]

hf = [(0, 0)]
hb = [(0, n*n-1)]
forward = {0:0}
backward = {n*n-1:0}

while hf and hb:
    costF, idxF = heappop(hf)
    iF, jF = divmod(idxF, n)
    costB, idxB = heappop(hb)
    iB, jB = divmod(idxB, n)

    mu = min(
        costF + backward.get(idxF, inf) - int(grid[iF][jF] == 'X'),
        costB + forward.get(idxB, inf) - int(grid[iB][jB] == 'X')
        )
    if mu < n * n + 1:
        # print(costF, backward.get(idxF, inf), iF, jF)
        # print(costB, forward.get(idxB, inf), iB, jB)
        print(mu) & exit()

    for di, dj in ((1,0),(0,1),(-1,0),(0,-1)):
        I, J = iF+di, jF+dj
        if 0<=I<n and 0<=J<n:
            newcostF = costF + int(grid[I][J] == 'X')
            if forward.get(I*n+J, inf) > newcostF:
                forward[I*n+J] = newcostF
                heappush(hf, (newcostF, I*n+J))

    for di, dj in ((1,0),(0,1),(-1,0),(0,-1)):
        I, J = iB+di, jB+dj
        if 0<=I<n and 0<=J<n:
            newcostB = costB + int(grid[I][J] == 'X')
            if backward.get(I*n+J, inf) > newcostB:
                backward[I*n+J] = newcostB
                heappush(hb, (newcostB, I*n+J))

"""
6
..X...
XXXXXX
.XXXXX
XXXX..
.XXX.X
..X...
=> 3
"""