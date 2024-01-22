#Minimum BFS Length
from sys import stdin , setrecursionlimit
setrecursionlimit(6 * (10 ** 4))
input = stdin.readline

def dfs(p , prev):
    for i in child[p]:
        if(i == prev):
            continue
        dfs(i , p)
        for k in range(1 , 21):
            for x in range(21):
                dp[p][k][x] += dp[i][k - 1][x]

def dfs1(p , prev):
    for i in child[p]:
        if(i == prev):
            continue

        pdp = []
        for k in range(21):
            pdp.append(dp[i][k][:])
            
        for k in range(1 , 21):
            for x in range(21):
                v = dp[p][k - 1][x]
                if(k - 2 >= 0):
                    v -= pdp[k - 2][x]
                dp[i][k][x] += v

        dfs1(i , p)

for T in range(int(input())):

    n = int(input())

    child = [[] for i in range(n + 1)]
    for i in range(n - 1):
        u , v = map(int,input().split())
        child[u].append(v)
        child[v].append(u)

    a = list(map(int,input().split()))

    dp = [[[0 for j in range(21)] for i in range(21)] for j in range(n + 1)]
    for i in range(1 , n + 1):
        for j in range(21):
            dp[i][0][j] = (a[i - 1] // (1 << j))

    dfs(1 , 0)
    dfs1(1 , 0)

    ans = [0]*(n+1)
    for i in range(1 , n + 1):
        for j in range(21):
            ans[i] += dp[i][j][j]

    print(*ans[1:])