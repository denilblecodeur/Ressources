def getPrimeFactors(n):
    res = {}
    if n % 2 == 0:
        res[2] = 0
        while n % 2 == 0:
            res[2] += 1
            n //= 2
    for i in range(3,int(n**.5)+1,2):
        if n % i == 0:
            res[i] = 0
            while n % i == 0:
                res[i] += 1
                n //= i
    if n > 1:
        res[n] = 1
    return res

def getDivisors(n):
    primeFactors = getPrimeFactors(n)
    res = []
    pw = 1
    for factor in primeFactors:
        pw *= primeFactors[factor] + 1
    for i in range(pw):
        divisor = 1
        for factor in primeFactors:
            divisor *= factor ** (i % (primeFactors[factor] + 1))
            i //= primeFactors[factor] + 1
        res.append(divisor)
    return res

def divisors(x):
    res = [x]
    for i in range(1, int(x**.5)+1):
        if x % i == 0:
            res.append(i)
            if i != x // i:
                res.append(x // i)
    return res

# SIEVE
maxn = 1000000
divisors = [[] for _ in range(maxn + 1)]
for i in range(1, maxn + 1):
    for j in range(i, maxn + 1, i):
        divisors[j].append(i)

MAXN = 2000000
spf = [-1] * (MAXN + 2)
for i in range(2, MAXN + 1):
    if spf[i] == -1:
        for j in range(i + i, MAXN + 1, i):
            spf[j] = i

def getnpf(x):
    pfac = defaultdict(int)
    while spf[x] != -1:
        pfac[spf[x]] += 1
        x //= spf[x]
    if x != 1:
        pfac[x] += 1
    tot, pf = 1, 0
    for k, v in pfac.items():
        tot *= (v + 1)
        pf += 1
    return tot - pf

# GET UNIQUE MULTIPLE COUNT

n, k = map(int,input().split())
pfac = list(map(int,input().split()))
 
ans = 0
for mask in range(1, 1<<k):
    num = 1
    for i in range(k):
        if mask >> i & 1:
            num *= pfac[i]
        if num > n:
            break
    if bin(mask).count('1') % 2:
        ans += n // num
    else:
        ans -= n // num
 
print(ans)