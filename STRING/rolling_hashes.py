import sys
input = sys.stdin.readline

MOD = 1_000_000_007
P1 = 31
P2 = 37

S = input().rstrip('\n')
N = len(S)
K = int(input())

idx = lambda c: ord(c) - 97 + 1

hashes1 = set()
hashes2 = set()
for _ in range(K):
    word = input().rstrip('\n')
    if len(word) > N:
        continue
    h1, h2 = 0, 0
    for c in word:
        h1 = (h1 * P1 + idx(c)) % MOD
        h2 = (h2 * P2 + idx(c)) % MOD
    hashes1.add(h1)
    hashes2.add(h2)

pow1 = [1] * (N + 1)
pow2 = [1] * (N + 1)
for i in range(N):
    pow1[i + 1] = (pow1[i] * P1) % MOD
    pow2[i + 1] = (pow2[i] * P2) % MOD

dp = [0] * (N + 1)
dp[0] = 1
sh1 = [0] * (N + 1)
sh2 = [0] * (N + 1)
h1, h2 = 0, 0

for r in range(1, N + 1):
    h1 = (h1 * P1 + idx(S[r - 1])) % MOD
    h2 = (h2 * P2 + idx(S[r - 1])) % MOD
    sh1[r] = h1
    sh2[r] = h2
    for l in range(r):
        pre_hash1 = (sh1[l] * pow1[r - l]) % MOD
        sub_hash1 = (sh1[r] - pre_hash1) % MOD
        pre_hash2 = (sh2[l] * pow2[r - l]) % MOD
        sub_hash2 = (sh2[r] - pre_hash2) % MOD
        if sub_hash1 in hashes1 and sub_hash2 in hashes2:
            dp[r] = (dp[r] + dp[l]) % MOD
 
print(dp[N])

# PREFIX - SUFFIX rolling hashes
# detects __ABC____CBA__
N = int(2e5)+2
MOD = 1_000_000_007
P1 = 37

pw = [1] * (N+1)
for i in range(N): pw[i + 1] = (pw[i] * P1) % MOD

n = len(s)

left = [0] * (n + 1)
right = [0] * (n + 1)
h_left = h_right = 0
for r in range(1, n + 1):
    left[r] = h_left = (h_left * P1 + s[r - 1]) % MOD
    right[r] = h_right = (h_right * P1 + s[n - r]) % MOD

def substrLeft(l, r): #0-ind
    return (left[r + 1] - (left[l] * pw[r - l + 1]) % MOD) % MOD

def substrRight(l, r): #0-ind
    return (right[n-l] - (right[n-1-r] * pw[r - l + 1]) % MOD) % MOD

l, r = 0, n-1
while l < r:
    pl, pr = l, r
    for x in range((r-l+1)//2 + 1):
        if l + x >= r - x: continue
        if substrLeft(l, l+x) == substrRight(l+x+1, l+2*x+1):
            l += x+1
            break
        elif substrLeft(r-2*x-1, r-x-1) == substrRight(r-x, r):
            r -= x+1
            break
    if l==pl and r==pr: break
print(r-l+1)