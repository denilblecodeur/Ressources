# Balanced tree that is simple and fast in practice
from bisect import bisect, bisect_left
class BTree:
    def __init__(self, capacity=512):
        self.nodes = [[]]
        self.capacity = capacity
    def __len__(self):
        return sum(len(n) for n in self.nodes)
    def __iter__(self):
        for n in self.nodes:
            for k in n:
                yield k
    def __reversed__(self):
        for n in reversed(self.nodes):
            for k in reversed(n):
                yield k
    def __repr__(self):
        return f"[{', '.join(self)}]"
    
    def add(self, key, overwrite=None): # use None for a multiset
        N, C = self.nodes, self.capacity
        i, n = next(((i, n) for i, n in enumerate(N) if n and n[-1]>=key), (len(N)-1, N[-1]))
        j = bisect(n, key)
        # use tuples for keys and update this equality to turn the set into a map
        if j > 0 and n[j-1] == key and overwrite is not None:
            n[j] = key if overwrite else n[j]
            return overwrite
        if len(n) == C:
            N[i] = n[C//2:]
            N.insert(i, n[:C//2])
            n, j = (N[i], j) if j<=C//2 else (N[i+1], j-C//2)
        n.insert(j, key)
        return True
    def get_lower(self, key, default=None, delete=False):
        n = next((n for n in reversed(self.nodes) if n and n[0]<=key), [])
        j = bisect(n, key) - 1
        return default if j<0 else n.pop(j) if delete else n[j]
    def get_upper(self, key, default=None, delete=False):
        n = next((n for n in self.nodes if n and n[-1]>=key), [])
        j = bisect_left(n, key)
        return default if j==len(n) else n.pop(j) if delete else n[j]

##### Persistent Braun tree ######

def add(tree, element, op):
    (key, value, left, right) = tree
    if key == element:
        return (key, value + op, left, right)
    if key > element:
        return (key, value, add(left, element, op), right)
    return (key, value + op, left, add(right, element, op))
        
def init(f, size):
    if f + 1 == size:
        return (f, 0, None, None)
    mid = (f + size) // 2
    return (mid, 0, init(f, mid), init(mid, size))

def query(tree, qk):
    (key, value, left, right) = tree
    if key == qk:
        return value
    if key > qk:
        return value + query(left, qk)
    return query(right, qk)

N = int(input())
S = [init(0, N + 1)]
for _ in range(N):
    S.append(S[-1])
    for el in input().split():
        S[-1] = add(S[-1], int(el[1:]), int(el[0]+'1'))

x = 0
for _ in range(N):
    x = (x + query(S[int(input())], x)) % N
print(x)