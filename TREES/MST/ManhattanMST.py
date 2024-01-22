import sys
input = sys.stdin.buffer.readline
import math
from typing import Generic, Iterable, Iterator, TypeVar, Union, List
from bisect import bisect_left, bisect_right

class ManhattanMST:
    def __init__(self) -> None:
        self.n = 0
        self.points = []
        self.edges = []

    def add_point(self, i, j):
        self.n += 1
        self.points.append(i)
        self.points.append(j)

    def sweep(self):
        m = SortedSet()
        d = {}
        for i in self.idx:
            x, y = self.points[i << 1], self.points[(i << 1) + 1]
            while m:
                z = m.le(y)
                if z is None:
                    break
                j = d[z]
                dx = x - self.points[j << 1]
                dy = y - self.points[(j << 1) + 1]
                if dy > dx:
                    break
                self.edges.append((dx + dy, i, j))
                m.discard(z)
                del d[z]
            m.add(y)
            d[y] = i

    def solve(self):
        for i in range(2):
            p_sum = [
                self.points[x << 1] + self.points[(x << 1) + 1] for x in range(self.n)
            ]
            self.idx = sorted(range(self.n), key=lambda x: p_sum[x])
            for _j in range(2):
                self.sweep()
                for j in range(self.n):
                    self.points[j << 1], self.points[(j << 1) + 1] = (
                        self.points[(j << 1) + 1],
                        self.points[j << 1],
                    )
            if not i:
                for j in range(self.n):
                    self.points[j << 1] *= -1
        self.edges.sort(key=lambda x: x[0])


class UnionFind:
    def __init__(self, n: int) -> None:
        self.n = n
        self.parent = [-1] * n
        self.groups = n

    def find(self, x: int) -> int:
        if self.parent[x] < 0:
            return x
        else:
            p = x
            while self.parent[p] >= 0:
                p = self.parent[p]
            while self.parent[x] >= 0:
                self.parent[x], x = p, self.parent[x]
            return p

    def union(self, x: int, y: int) -> bool:
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self.parent[x] > self.parent[y]:
            x, y = y, x
        self.parent[x] += self.parent[y]
        self.parent[y] = x
        self.groups -= 1
        return True

T = TypeVar("T")

class SortedSet(Generic[T]):
    # https://github.com/tatyam-prime/SortedSet/blob/main/SortedSet.py
    BUCKET_RATIO = 75
    REBUILD_RATIO = 255

    def _build(self, a=None) -> None:
        "Evenly divide `a` into buckets."
        if a is None:
            a = list(self)
        size = self.size = len(a)
        bucket_size = int(math.ceil(math.sqrt(size / self.BUCKET_RATIO)))
        self.a = [
            a[size * i // bucket_size : size * (i + 1) // bucket_size]
            for i in range(bucket_size)
        ]

    def __init__(self, a: Iterable[T] = []) -> None:
        "Make a new SortedSet from iterable. / O(N) if sorted and unique / O(N log N)"
        a = list(a)
        if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
            a = sorted(set(a))
        self._build(a)

    def __iter__(self) -> Iterator[T]:
        for i in self.a:
            for j in i:
                yield j

    def __reversed__(self) -> Iterator[T]:
        for i in reversed(self.a):
            for j in reversed(i):
                yield j

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return "SortedSet" + str(self.a)

    def __str__(self) -> str:
        s = str(list(self))
        return "{" + s[1 : len(s) - 1] + "}"

    def _find_bucket(self, x: T) -> List[T]:
        "Find the bucket which should contain x. self must not be empty."
        for a in self.a:
            if x <= a[-1]:
                return a
        return a

    def __contains__(self, x: T) -> bool:
        if self.size == 0:
            return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        return i != len(a) and a[i] == x

    def add(self, x: T) -> bool:
        "Add an element and return True if added. / O(√N)"
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return True
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return False
        a.insert(i, x)
        self.size += 1
        if len(a) > len(self.a) * self.REBUILD_RATIO:
            self._build()
        return True

    def discard(self, x: T) -> bool:
        "Remove an element and return True if removed. / O(√N)"
        if self.size == 0:
            return False
        a = self._find_bucket(x)
        i = bisect_left(a, x)
        if i == len(a) or a[i] != x:
            return False
        a.pop(i)
        self.size -= 1
        if len(a) == 0:
            self._build()
        return True

    def lt(self, x: T) -> Union[T, None]:
        "Find the largest element < x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] < x:
                return a[bisect_left(a, x) - 1]

    def le(self, x: T) -> Union[T, None]:
        "Find the largest element <= x, or None if it doesn't exist."
        for a in reversed(self.a):
            if a[0] <= x:
                return a[bisect_right(a, x) - 1]

    def gt(self, x: T) -> Union[T, None]:
        "Find the smallest element > x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] > x:
                return a[bisect_right(a, x)]

    def ge(self, x: T) -> Union[T, None]:
        "Find the smallest element >= x, or None if it doesn't exist."
        for a in self.a:
            if a[-1] >= x:
                return a[bisect_left(a, x)]

    def __getitem__(self, x: int) -> T:
        "Return the x-th element, or IndexError if it doesn't exist."
        if x < 0:
            x += self.size
        if x < 0:
            raise IndexError
        for a in self.a:
            if x < len(a):
                return a[x]
            x -= len(a)
        raise IndexError

    def index(self, x: T) -> int:
        "Count the number of elements < x."
        ans = 0
        for a in self.a:
            if a[-1] >= x:
                return ans + bisect_left(a, x)
            ans += len(a)
        return ans

    def index_right(self, x: T) -> int:
        "Count the number of elements <= x."
        ans = 0
        for a in self.a:
            if a[-1] > x:
                return ans + bisect_right(a, x)
            ans += len(a)
        return


for _ in range(int(input())):
    r, c, n = map(int, input().split())
    m = ManhattanMST()
    src, snk = None, None
    for i in range(n):
        x, y = map(int, input().split())
        m.add_point(x, y)
        if x == y == 1:
            src = i
        if x == r and y == c:
            snk = i
    u = UnionFind(n)
    graph = [[] for _ in range(n)]
    m.solve()
    for d, i, j in m.edges:
        if u.union(i, j):
            graph[i].append((j, d))
            graph[j].append((i, d))
    
    par = [None] * n
    Q = [src]
    while Q:
        v = Q.pop()
        for u, d in graph[v]:
            if par[v] is None or u != par[v][0]:
                Q.append(u)
                par[u] = (v, d)
    v = snk
    ans = 0
    while v != src:
        v, d = par[v]
        ans = max(ans, d)
        
    print(ans // 2)