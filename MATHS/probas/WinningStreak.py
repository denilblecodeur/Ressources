# https://lbv-pc.blogspot.com/2012/06/winning-streak.html
import sys
input = sys.stdin.buffer.readline

while True:
    n, p = input().split()
    n, p = int(n), float(p)
    if n == 0: break

    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    for j in range(n + 1):
        dp[0][j] = 1
    
    for i in range(1, n + 1):
        for j in range(n + 1):
            dp[i][j] = dp[i - 1][j]
            if j == i - 1:
                dp[i][j] -= p**i
            elif j < i - 1:
                dp[i][j] -= dp[i - j - 2][j] * (1 - p) * p**(j + 1)
    
    ans = 0
    for j in range(n + 1):
        ans += j * (dp[n][j] - dp[n][j - 1])
    print(ans)