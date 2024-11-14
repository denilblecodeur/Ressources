# https://codeforces.com/contest/1215/problem/E

def GospersHack(k,n):
    # génère toutes les combinaisons possibles de k bits parmi n bits
    if k==0: yield 0
    cur=(1<<k)-1
    while 0<cur<1<<n:
        yield cur
        lb=cur&-cur
        r=cur+lb
        cur=(r^cur)>>lb.bit_length()+1|r
        
n = int(input())
a = [int(x)-1 for x in input().split()]
N, ALLSET = 20, 0
cost = [[0] * N for _ in range(N)]
cnt = [0] * N
for i in range(n):
    ALLSET |= (1<<a[i])
    for col in range(N):
        cost[a[i]][col] += cnt[col]
    cnt[a[i]] += 1
dp = [1<<59] * (1<<N)
dp[0] = 0
for mask in range(1, 1<<N):
    for col1 in range(N):
        if mask>>col1&1 == 0: continue
        c = 0
        for col2 in range(N):
            if mask>>col2&1: continue
            c += cost[col1][col2]
        dp[mask] = min(dp[mask], dp[mask ^ (1<<col1)] + c)
print(dp[ALLSET])
