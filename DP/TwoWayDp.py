"""
INF = 1000001

n,m  = map(int,input().split())
coins = list(map(int,input().split()))

dp = [INF]*(m+1)
dp[0] = 0
for i in range(m):
    for c in coins:
"""
if i - c >= 0:
    dp[i] = min(dp[i], dp[i - c] + 1)
if i + c <= m:
    dp[i + c] = min(dp[i + c], dp[i] + 1)

"""
print(dp[m] if dp[m] != INF else -1)
"""