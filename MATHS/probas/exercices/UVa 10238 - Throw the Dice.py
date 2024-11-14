import sys
ans = []
for line in sys.stdin.buffer:
    F, N, S = map(int,line.split())
    dp = [0] * (S+1)
    dp[0] = 1
    for _ in range(N):
        nextdp = [0] * (S+1)
        for result in range(1, F+1):
            for sum_ in range(S-result+1):
                nextdp[sum_ + result] += dp[sum_]
        dp = nextdp
    ans.append("{}/{}".format(dp[S], F**N))
print(*ans, sep='\n')