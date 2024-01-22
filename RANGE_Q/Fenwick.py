# FENWICK point update range query

def update(pos, v):
    while pos < n:
        T[pos] += v
        pos |= pos + 1

def _query(pos):
    r = 0
    while pos:
        r += T[pos-1]
        pos &= pos-1
    return r

def query(a, b): # [l, r)
    return _query(b) - _query(a)

n, q = map(int,input().split())
X = [int(input()) for _ in range(n)]
T = list(X)
for i in range(n):
    j = i | (i+1)
    if j < n: T[j] += T[i]
query(l, r + 1) # [l, r] 0-indexed
update(pos, newvalue - X[pos]); X[pos] = newvalue # pos 0-indexed

# FENWICK 1-indexed rangesum rangequery

def add(b, idx, v):
    while idx <= n:
        b[idx] += v
        idx += idx & -idx

def range_add(l, r, v):
    j = l
    while j <= n:
        B1[j] += v
        B2[j] += v * (l - 1)
        j += j & -j
    j = r + 1
    while j <= n:
        B1[j] -= v
        B2[j] -= v * r
        j += j & -j

def _query(b, idx):
    total = 0
    while idx > 0:
        total += b[idx]
        idx -= idx & -idx
    return total

def prefix_sum(idx):
    return _query(B1, idx) * idx - _query(B2, idx)

def range_sum(l, r):
    return prefix_sum(r) - prefix_sum(l - 1)

n, q = map(int,input().split())
X = list(map(int,input().split()))
B1, B2 = [0] * (n + 1), [0] * (n + 1)
for i, v in enumerate(X, 1):
    range_add(i, i, v)
for _ in range(q):
    line = map(int,input().split())
    if next(line) == 1:
        a, b = line
        print(range_sum(a, b))
    else:
        a, b, v = line
        range_add(a, b, v)