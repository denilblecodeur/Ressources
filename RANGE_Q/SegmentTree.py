# SEGMENT TREE 0-indexed

def update(p, val):
    p += N
    seg[p] = val
    while p > 1:
        seg[p>>1] = seg[p] + seg[p^1]
        p >>= 1

def query(l, r): # [l, r)
    res = 0
    l += N; r += N
    while l < r:
        if l&1: res += seg[l]; l += 1
        if r&1: r -= 1; res += seg[r]
        l >>= 1; r >>= 1
    return res

N = 1 << n.bit_length()
seg = [0] * (2 * N)
for i in range(n):
    seg[N + i] = a[i]
for k in range(N - 1, 0, -1):
    seg[k] = seg[k<<1] + seg[k<<1|1]

update(n - 1, 0)
print(query(0, n))

# RANGE UPDATE, POINT QUERY

def update(l, r, val): # [l, r)
    l += N; r += N
    while l < r:
        if l&1: seg[l] += val; l += 1
        if r&1: r -= 1; seg[r] += val
        l >>= 1; r >>= 1

def query(p):
    res = 0
    p += N
    while p > 0:
        res += seg[p]
        p >>= 1
    return res

# reduce the complexity from O(nlog(n)) to O(n) to get all values.
# works only in case the order of modifications on a single element doesn't affect the result.
def push():
    for i in range(1, N):
        seg[i<<1] += seg[i]
        seg[i<<1|1] += seg[i]
        seg[i] = 0

n = int(input())
a = list(map(int,input().split()))
N = 2 ** n.bit_length()
seg = [0] * (2 * N)
for i in range(n):
    seg[N + i] = a[i]
""" supprimer ligne 
for k in range(N - 1, 0, -1):
    seg[k] = seg[k<<1] + seg[k<<1|1]
"""

update(0, n, 5)
push()
for i in range(n):
    print(seg[N + i])

# return index
class SegTree: 
    def __init__(self, a):
        self.arr = a[:]
        self.n = len(a)
        self.t = [0] * 2 * self.n
        for i in range(self.n):
            self.t[self.n + i] = i
        for i in range(self.n - 1, 0, -1):
            self.t[i] = min(self.t[i << 1], self.t[(i << 1) | 1], key=lambda x:self.arr[x])
    
    def update(self, pos, val):
        i = pos + self.n
        self.arr[self.t[i]] = val
        while i > 1:
            self.t[i >> 1] = min(self.t[i], self.t[i ^ 1], key=lambda x:self.arr[x])
            i >>= 1
    
    def query(self, l, r): # [l, r]
        ans = 0
        l += self.n
        r += self.n + 1
        while l < r:
            if (l & 1):
                ans = min(ans, self.t[l], key=lambda x:self.arr[x])
                l += 1
            if (r & 1):
                r -= 1
                ans = min(ans, self.t[r], key=lambda x:self.arr[x])
            l >>= 1
            r >>= 1
        return ans

#return value
class SegTree: 
    def __init__(self, a):
        self.n = len(a)
        self.t = [0] * 2 * self.n
        for i in range(self.n):
            self.t[self.n + i] = a[i]
        for i in range(self.n - 1, 0, -1):
            self.t[i] = min(self.t[i << 1], self.t[(i << 1) | 1])
    
    def update(self, pos, val):
        i = pos + self.n
        self.t[i] = val
        while i > 1:
            self.t[i >> 1] = min(self.t[i], self.t[i ^ 1])
            i >>= 1
    
    def query(self, l, r):
        # minimum min(a[l], ... , a[r])
        ans = 1<<59
        l += self.n
        r += self.n + 1
        while l < r:
            if (l & 1):
                ans = min(ans, self.t[l])
                l += 1
            if (r & 1):
                r -= 1
                ans = min(ans, self.t[r])
            l >>= 1
            r >>= 1
        return ans