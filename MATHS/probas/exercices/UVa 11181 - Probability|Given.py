def compute(n, r, p, chosen=None):
    dp = [[0] * (r+1) for _ in range(n+1)]
    dp[0][0] = 1
    for i in range(1, n+1):
        for j in range(min(i, r)+1):
            if chosen != i:
                dp[i][j] += dp[i-1][j] * (1-p[i-1])
            if j>0:
                dp[i][j] += dp[i-1][j-1] * p[i-1]
    return dp[n][r]

tc = 0
while True:
    tc += 1
    n, r = map(int,input().split())
    if n == r == 0: break
    p = [float(input()) for _ in range(n)]
    prob_tot = compute(n, r, p)
    print("Case {}:".format(tc))
    for i in range(n):
        # P(b | a) = P(a et b) / P(a)
        print("{:.06f}".format(compute(n, r, p, i+1) / prob_tot))

"""
Alternative AC sans dp, O(C(n,r) * n), 3.7e6 op en pratique

def GospersHack(k,n):
    if k==0: yield 0
    cur=(1<<k)-1
    while 0<cur<1<<n:
        yield cur
        lb=cur&-cur
        r=cur+lb
        cur=(r^cur)>>lb.bit_length()+1|r

tc = 0
while True:
    tc += 1
    n, r = map(int,input().split())
    if n == r == 0: break
    p = [float(input()) for _ in range(n)]
    prob_tot = 0
    contrib = [0] * n
    for mask in GospersHack(r, n):
        prob = 1
        for b in range(n):
            if mask>>b&1:
                prob *= p[b]
            else:
                prob *= (1-p[b])
        prob_tot += prob
        for b in range(n):
            if mask>>b&1:
                contrib[b] += prob

    print("Case {}:".format(tc))
    for i in range(n):
        # P(b | a) = P(a et b) / P(a)
        print("{:.06f}".format(contrib[i] / prob_tot))
"""