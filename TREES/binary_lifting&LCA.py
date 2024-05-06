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
    if depth[a] < depth[b]: a, b = b, a
    k = depth[a] - depth[b]
    for j in range(LOG):
        if k & (1<<j): a = up[a][j]
    if a == b: return a
    for j in range(LOG - 1, -1, -1):
        if up[a][j] != up[b][j]:
            a, b = up[a][j], up[b][j]
    return up[a][0]

def get_kth_ancestor(a, k):
    if depth[a] < k: return -1
    for j in range(LOG):
        if k >> j & 1: node = up[node][j]
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
        assert 0 <= begin < end <= len(self._data)
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
        if a > b: a, b = b, a
        # psum[b + 1] to include b, psum[a] to include a
        return self.psum[b] - self.psum[a + 1]
    
    def distance(self, a, b):
        return self.depth[a] + self.depth[b] - 2 * self.depth[self(a, b)]
 
    def __call__(self, a, b):
        if a == b: return a
        a = self.time[a]
        b = self.time[b]
        if a > b: a, b = b, a
        return self.path[self.rmq.query(a, b)]

""" calc max edge on path """
class LcaDoubling:
    def __init__(self, n, graph, root=1, lcaf=max):
        # vertexes 1-indexed, graph[v] = [[u,w],[u,w],...]
        self.lcaf = lcaf
        self.e = -(1<<60) if lcaf == max else (1<<60)
        # depth and distance from the roots
        self.depths = [-1] * (n+1)
        self.distances = [-1] * (n+1)
        # self.ancestors[k][v]:Parent 2^k away from vertex v,
        # self.funcs[k][v]:Max(min) cost of an edge on the path from vertex v to its parent 2^k away
        prev_ancestors, prev_funcs = self._init_dfs(n, graph, root)
        self.ancestors = [prev_ancestors]
        self.funcs = [prev_funcs]
        max_depth = max(self.depths)
        d = 1
        while d < max_depth:
            next_ancestors = []
            next_funcs = []
            for i in range(len(prev_ancestors)):
                p = prev_ancestors[i]
                dist = prev_funcs[i]
                next_ancestors.append(prev_ancestors[p])
                next_funcs.append(self.lcaf(dist, prev_funcs[p]))
            self.ancestors.append(next_ancestors)
            self.funcs.append(next_funcs)
            d <<= 1
            prev_ancestors = next_ancestors
            prev_funcs = next_funcs
 
    def _init_dfs(self, n, graph, root):
        que = [(root, -1, 0, 0)]
        direct_ancestors = [-1 for i in range(n+2)]
        direct_funcs = [self.e for i in range(n+2)]
        self.depths[root] = 0
        self.distances[root] = 0
        while que:
            crr, pre, dep, dist = que.pop()
            for nxt, w in graph[crr]:
                if nxt == pre:
                    continue
                direct_ancestors[nxt] = crr
                direct_funcs[nxt] = w
                self.depths[nxt] = dep + 1
                self.distances[nxt] = dist + w
                que.append((nxt, crr, dep + 1, dist+w))
        return direct_ancestors, direct_funcs
 
    def upstream(self, v, k):
        fans = self.e
        b = 0
        while k:
            if k & 1:
                fans = self.lcaf(fans, self.funcs[b][v])
                v = self.ancestors[b][v]
            k >>= 1
            b += 1
        return v, fans
 
    def get_lca(self, u, v):
        du, dv = self.depths[u], self.depths[v]
        if du > dv: u, v, du, dv = v, u, dv, du
        tu = u
        tv, _ = self.upstream(v, dv-du)
        if tu == tv: return tu
        for k in range(du.bit_length())[::-1]:
            mu = self.ancestors[k][tu]
            mv = self.ancestors[k][tv]
            if mu != mv: tu, tv = mu, mv
        lca = self.ancestors[0][tu]
        return lca
 
    def get_distance(self, u, v):
        return self.distances[u] + self.distances[v] - 2 * self.distances[self.get_lca(u, v)]
 
    def get_lcaf(self, u, v):
        # get lcaf from u to lca(u, v)
        # and from v to lca(u, v)
        lca = self.get_lca(u, v)
        du = self.depths[u] - self.depths[lca]
        dv = self.depths[v] - self.depths[lca]
        _, uans = self.upstream(u, du)
        _, vans = self.upstream(v, dv)
        return self.lcaf(vans, uans)