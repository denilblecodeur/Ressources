def edit_dist(a, b):
    if len(a) > len(b):
        a, b = b, a
    dp = [[1<<20] * (len(a) + 1) for _ in range(len(b) + 1)]
    dp[0][0] = 0
    for i in range(1, len(b) + 1):
        if i < len(a) + 1:
            dp[0][i] = i
        dp[i][0] = i

    for i in range(1, len(b) + 1):
        for j in range(1, len(a) + 1):
            # suppression, ajout, match ou remplace
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + int(a[j - 1] != b[i - 1]))
    
    return dp[len(b)][len(a)]