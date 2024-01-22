from sys import stdin, stdout

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

class Segment:
    def __init__(self, ax, ay, bx, by):
        self.a = (ax, ay)
        self.b = (bx, by)

def main():
    def intersect(a,b,c,d):
        def ccw(a,b,c):
            cp = (a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0])
            return 1 if cp > 0 else -1 if cp < 0 else 0
        def onSegment(a,b,c):
            in_x = min(a[0],b[0]) <= c[0] <= max(a[0],b[0])
            in_y = min(a[1],b[1]) <= c[1] <= max(a[1],b[1])
            return in_x and in_y
        if not (ccw(a,b,c) or ccw(a,b,d) or ccw(b,c,d) or ccw(a,c,d)):
            return onSegment(a,b,c) or onSegment(a,b,d) or onSegment(c,d,b) or onSegment(c,d,a)
        return ccw(a,b,c) != ccw(a,b,d) and ccw(b,c,d) != ccw(a,c,d)

    for _ in range(int(stdin.readline())):
        n, m = map(int,stdin.readline().split())
        uf = UnionFind(n)
        seg = [Segment(*map(int,stdin.readline().split())) for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j:
                    u = uf.find(i)
                    v = uf.find(j)
                    if u != v and intersect(seg[i].a, seg[i].b, seg[j].a, seg[j].b):
                        uf.union(u, v)

        for _ in range(m):
            x, y = map(int,stdin.readline().split())
            if uf.find(x - 1) == uf.find(y - 1):
                stdout.write('YES\n')
            else:
                stdout.write('NO\n')
main()