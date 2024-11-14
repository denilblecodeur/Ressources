s = input()
n = len(s)
dp = [[[1<<59] * k for _ in range(n)] for _ in range(n)]
for i in range(n):
    dp[i][i][chars.find(s[i])] = 0
for span in range(1, n):
    for l in range(n - span):
        # dp[l][l+span][z] = min| dp[l][l+d][x] + dp[l+d+1][l+span][y] + cost(x,y) if x+y -> z
        for d in range(span):
            for x in range(k):
                for y in range(k):
                    c, z = rule[x][y]
                    dp[l][l+span][z] = min(dp[l][l+span][z], dp[l][l+d][x] + dp[l+d+1][l+span][y] + c)
bestcost = float('inf')
best = None
for char in chars:
    if bestcost > dp[0][n-1][chars.find(char)]:
        bestcost = dp[0][n-1][chars.find(char)]
        best = char