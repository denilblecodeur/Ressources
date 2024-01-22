grid = [list(input()) for _ in range(h)]

dp = [[0] * (w + 1) for _ in range(h + 1)]
for i in range(1, max(w, h) + 1):
    if i < h + 1:
        dp[i][1] = int(grid[i - 1][0] == '#')
        dp[i][1] += dp[i - 1][1]
    if i < w + 1:
        dp[1][i] = int(grid[0][i - 1] == '#')
        dp[1][i] += dp[1][i - 1]

for i in range(2, h + 1):
    for j in range(2, w + 1):
        dp[i][j] = int(grid[i - 1][j - 1] == '#')
        dp[i][j] += dp[i - 1][j] + dp[i][j - 1] - dp[i - 1][j - 1]

area_of_k_k = dp[i + k][j + k] - dp[i][j + k] - dp[i + k][j] + dp[i][j]