# https://lbv-pc.blogspot.com/2012/06/winning-streak.html
import sys

for line in sys.stdin.buffer:
    n, p = line.split()
    n, p = int(n), float(p)
    if n == 0: break
    dp = [[0] * (n+1) for _ in range(n+1)]
    
    for i in range(n+1):
        for j in range(i, n+1):
            dp[i][j] = 1
        if i>0:
            dp[i][i-1] = (1 - p**i)

    for i in range(1, n+1):
        for j in range(i):
            dp[i][j] = dp[i-1][j]
            if j == i-1:
                dp[i][j] -= p**(j+1)
            else:
                dp[i][j] -= dp[i-j-2][j] * (1-p) * p**(j+1)
    
    ans = 0
    for j in range(1, n+1):
        ans += j * (dp[n][j] - dp[n][j-1])
    print(ans)