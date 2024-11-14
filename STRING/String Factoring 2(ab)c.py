n = int(input())
s = input()

def prefix(s):
    n = len(s)
    pi = [0 for i in range(n)]
    for i in range(1,n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi[-1]

dp = [[701] * (n + 1) for _ in range(n + 1)]

for l in range(1, n + 1):
    for i in range(n - l + 1):
        j = i + l - 1
        if i == j:
            dp[i][j] = 1
            continue
        for k in range(i, j):
            dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j])

        pref = prefix(s[i : i + l])
        if l % (l - pref) == 0:
            dp[i][j] = min(dp[i][j], dp[i][i + l - pref - 1])
        
print(dp[0][n - 1])