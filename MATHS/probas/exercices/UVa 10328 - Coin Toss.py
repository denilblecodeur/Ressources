# https://algorithmist.com/wiki/UVa_10328_-_Coin_Toss
import sys

dp = [[0] * 101 for _ in range(101)]
for k in range(1, 101):
    for i in range(k-1, 100):
        dp[k][i+1] = 2 * dp[k][i]
        if i == k-1:
            dp[k][i+1] += 1
        else:
            dp[k][i+1] += (1<<(i-k)) - dp[k][i-k]

for line in sys.stdin.buffer:
    n, k = map(int,line.split())
    print(dp[k][n])

"""
Alternative: calculate directly, O(n^3)

dp = [[[0] * 101 for _ in range(101)] for _ in range(101)]
dp[0][0][0] = 1
for i in range(100):
    for m in range(i+1):
        for c in range(m+1):
            # TAIL
            dp[i+1][m][0] += dp[i][m][c]
            # HEAD
            if c == m:
                dp[i+1][m+1][c+1] += dp[i][m][c]
            else:
                dp[i+1][m][c+1] += dp[i][m][c]

ans = [[0] * 101 for _ in range(101)]
for i in range(1, 101):
    for m in reversed(range(i+1)):
        ans[i][m] = sum(dp[i][m])
        if m+1 <= i:
            ans[i][m] += ans[i][m+1]
"""