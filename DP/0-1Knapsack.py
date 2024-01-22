#0-1 Knapsack 2D
n, x = map(int,input().split())
price = list(map(int,input().split()))
pages = list(map(int,input().split()))

dp = [[0] * (x + 1) for _ in range(n + 1)]

for i in range(1, n + 1):
    for j in range(x + 1):
        dp[i][j] = dp[i - 1][j]
        left = j - price[i - 1]
        if left >= 0:
            dp[i][j] = max(dp[i][j], dp[i - 1][left] + pages[i - 1])
print(dp[n][x])

#0-1 Knapsack 1D
n, x = map(int,input().split())
price = list(map(int,input().split()))
page = list(map(int,input().split()))
dp = [0] * (x + 1)
for k, v in zip(price, page):
    for j in range(x, k - 1, -1):
        dp[j] = max(dp[j], dp[j - k] + v)
print(dp[x])