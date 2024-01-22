class DSU:
    def __init__(self, n):
        self.up = list(range(n))
        self.size = [1] * n
 
    def find(self, x):
        if self.up[x] != x:
            self.up[x] = self.find(self.up[x])
        return self.up[x]
 
    def union(self, x, y):
        x, y = self.find(x), self.find(y)
        if x == y:
            return False
        if self.size[x] < self.size[y]:
            x, y = y, x
        self.up[y] = x
        self.size[x] += self.size[y]
        return True

class UnionFind:
    def __init__(self, n):
        self.up = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.up[x] == x:
            return x
        else:
            self.up[x] = self.find(self.up[x])
            return self.up[x]
    
    def union(self, x, y):
        repr_x = self.find(x)
        repr_y = self.find(y)
        if repr_x == repr_y:
            return False
        if self.rank[repr_x] == self.rank[repr_y]:
            self.rank[repr_x] += 1
            self.up[repr_y] = repr_x
        elif self.rank[repr_x] > self.rank[repr_y]:
            self.up[repr_y] = repr_x
        else:
            self.up[repr_x] = repr_y
        return True

#100ms faster on average
class UnionFind():
    def __init__(self, n):
        self.n = n
        self.root = [-1] * n

    def union(self, a, b):
        x = self.find(a)
        y = self.find(b)
        if x == y: return x
        if -self.root[x] < -self.root[y]: x, y = y, x
        self.root[x] += self.root[y]
        self.root[y] = x
        return x

    def same(self, a, b):
        return self.find(a) == self.find(b)

    def find(self, a):
        x = a
        while self.root[x] >= 0:
            x = self.root[x]
        while self.root[a] >= 0:
            self.root[a] = x
            a = self.root[a]
        return x

    def size(self, a):
        return -self.root[self.find(a)]

    def groups(self):
        repr_buf = [0] * self.n
        group_size = [0] * self.n
        res = [[] for _ in range(self.n)]
        for i in range(self.n):
            repr_buf[i] = self.find(i)
            group_size[repr_buf[i]] += 1
        for i in range(self.n):
            res[repr_buf[i]].append(i)
        res = [res[i] for i in range(self.n) if res[i]]
        return res