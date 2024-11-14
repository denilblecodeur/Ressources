n = 16
cn = [input() for _ in range(n)]
p = [[float(x)/100 for x in input().split()] for _ in range(n)]
dp = [[0] * n for _ in range(5)]
dp[0] = [1] * n

for game in range(1, 5):
    for slot in range(0, n, 1<<game):
        for i in range(slot, slot+(1<<game>>1)):
            for j in range(slot+(1<<game>>1), slot+(1<<game)):
                dp[game][i] += dp[game-1][i] * dp[game-1][j] * p[i][j]
                dp[game][j] += dp[game-1][i] * dp[game-1][j] * p[j][i]

for c in range(n):
    print(str(cn[c]).ljust(10, " "), "p={:.02f}%".format(dp[4][c]*100))