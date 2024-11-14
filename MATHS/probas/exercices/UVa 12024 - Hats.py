import sys
input = sys.stdin.buffer.readline

fac = [1] * 13
for i in range(2, 13):
    fac[i] = fac[i-1] * i

dp = [0] * 13
dp[0] = 1
for i in range(2, 13):
    dp[i] = (i-1) * (dp[i-1] + dp[i-2])

for _ in range(int(input())):
    n = int(input())
    print("{}/{}".format(dp[n], fac[n]))