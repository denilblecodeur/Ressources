import sys
input = sys.stdin.buffer.readline
 
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
def query(a, b):
    return _query(b) - _query(a)
 
n, q = map(int,input().split())
val = list(map(int,input().split()))
 
tree = [[] for _ in range(n)]
for _ in range(n - 1):
    a, b = map(int,input().split())
    tree[a - 1].append(b - 1)
    tree[b - 1].append(a - 1)
 
prev = [None] * n
sz = [1] * n
ts = [-1] * n
ts[0] = 0
Q = [0]
order = []
while Q:
    v = Q[-1]
    if ts[v] == len(tree[v]):
        for u in tree[v]:
            if u == prev[v]:
                continue
            sz[v] += sz[u]
        order.append(v)
        Q.pop()
    else:
        u = tree[v][ts[v]]
        if u == prev[v]:
            ts[v] += 1
            if ts[v] == len(tree[v]):
                continue
            u = tree[v][ts[v]]
        ts[v] += 1
        ts[u] = 0
        prev[u] = v
        Q.append(u)
 
order.reverse()
index = {e:i for i, e in enumerate(order)}
val = [val[i] for i in order]
T = list(val)
for i, v in enumerate(val):
    j = i | (i+1)
    if j < n: T[j] += T[i]
 
for _ in range(q):
    line = map(int,input().split())
    if next(line) == 1:
        u, x = line
        update(index[u - 1], x - val[index[u - 1]])
        val[index[u - 1]] = x
    else:
        u, = line
        print(query(index[u - 1], index[u - 1] + sz[u - 1]))