import sys
input = sys.stdin.buffer.readline

for tc in range(int(input())):
    n, k, m = map(int,input().split())
    p = [float(input()) for _ in range(n)]
    if m == 0:
        print("Case #{}: {:.07f}".format(tc+1, int(k == 0)))
        continue
    dp = [0] * m
    dp[0] = p[0]
    for i in range(1, m):
        for j in range(n):
            dp[i] += p[j] * dp[i-1] ** j
    print("Case #{}: {:.07f}".format(tc+1, dp[m-1] ** k))