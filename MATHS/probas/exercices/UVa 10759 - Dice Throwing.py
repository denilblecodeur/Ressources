import sys, math

for line in sys.stdin.buffer:
    n, x = map(int,line.split())
    if n == x == 0: break
    if x == 0:
        print(1)
        continue
    dp = [0] * x
    dp[0] = 1
    for _ in range(n):
        nextdp = [0] * x
        for i in range(x):
            for result in range(1, 7):
                if i + result < x:
                    nextdp[i + result] += dp[i]
        dp = nextdp
    p, q = sum(dp), pow(6, n)
    g = math.gcd(p, q)
    if q//g == 1:
        print(q//g - p//g)
    else:
        print(q//g - p//g, q//g, sep='/')