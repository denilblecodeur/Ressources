n = int(input())
grid = [input() for _ in range(n)]
dp = [[0] * n for _ in range(n)]
dp[0][0] = 1 if grid[0][0] != '*' else 0
for i in range(n):
    for j in range(n):
        if i + 1 < n and grid[i + 1][j] != '*':
            dp[i + 1][j] += dp[i][j]
        if j + 1 < n and grid[i][j + 1] != '*':
            dp[i][j + 1] += dp[i][j]
print(dp[n - 1][n - 1])