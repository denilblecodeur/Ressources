LOG = n.bit_length()
up = [[0] * LOG for _ in range(n)]
depth = [0] * n
for node in range(1, n):
    up[node][0] = prev[node]
    depth[node] = depth[prev[node]] + 1
for k in range(1, LOG):
    for node in range(1, n):
        up[node][k] = up[up[node][k - 1]][k - 1]

def get_lca(a, b):
    if depth[a] < depth[b]:
        a, b = b, a
    k = depth[a] - depth[b]
    for j in range(LOG):
        if k & (1<<j):
            a = up[a][j]
    if a == b:
        return a
    for j in range(LOG - 1, -1, -1):
        if up[a][j] != up[b][j]:
            a = up[a][j]
            b = up[b][j]
    return up[a][0]

def get_kth_ancestor(a, k):
    if depth[a] < k:
        return -1
    for j in range(LOG):
        if k >> j & 1:
            node = up[node][j]
    return node

# FASTER
LOG = 30
n, q = map(int,input().split())
up = [[int(x) - 1 for x in input().split()]]
queries = [int(x) for x in sys.stdin.buffer.read().split()]
for _ in range(1, LOG):
    up.append([up[-1][up[-1][node]] for node in range(n)])
for i in range(0, len(queries), 2):
    x, k = queries[i] - 1, queries[i + 1]
    for j in range(LOG):
        if k >> j & 1:
            x = up[j][x]
    print(x + 1)

# CLASS LCA
lca = LCA(root=0, graph=g)

class RangeQuery:
    def __init__(self, data, func=min):
        self.func = func
        self._data = _data = [list(data)]
        i, n = 1, len(_data[0])
        while 2 * i <= n:
            prev = _data[-1]
            _data.append([func(prev[j], prev[j + i]) for j in range(n - 2 * i + 1)])
            i <<= 1
 
    def query(self, begin, end):
        depth = (end - begin).bit_length() - 1
        return self.func(self._data[depth][begin], self._data[depth][end - (1 << depth)])
 
 
class LCA:
    def __init__(self, root, graph):
        self.time = [-1] * len(graph)
        self.path = [-1] * len(graph)
        self.depth = [0] * len(graph)
        P = [-1] * len(graph)
        t = -1
        dfs = [root]
        while dfs:
            node = dfs.pop()
            self.path[t] = P[node]
            self.time[node] = t = t + 1
            for nei in graph[node]:
                if self.time[nei] == -1:
                    P[nei] = node
                    self.depth[nei] = self.depth[node] + 1
                    dfs.append(nei)
        self.rmq = RangeQuery(self.time[node] for node in self.path)
        # calc sum on a path
        # self.psum = [0] + list(accumulate(value[node] for node in self.path))
    
    # calc sum on a path
    def query(self, a, b):
        assert a != b
        a = self.time[a]
        b = self.time[b]
        if a > b:
            a, b = b, a
        # psum[b + 1] to include b, psum[a] to include a
        return self.psum[b] - self.psum[a + 1]
    
    def distance(self, a, b):
        return self.depth[a] + self.depth[b] - 2 * self.depth[self(a, b)]
 
    def __call__(self, a, b):
        if a == b:
            return a
        a = self.time[a]
        b = self.time[b]
        if a > b:
            a, b = b, a
        return self.path[self.rmq.query(a, b)]