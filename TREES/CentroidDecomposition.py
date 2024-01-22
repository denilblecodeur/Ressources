# E. Xenia and Tree

class CentroidDecomposition:
    def __init__(self, graph):
        self.graph = graph
        self.n = len(graph)
 
        self.parent = [-1] * self.n
        self.subtree = [1] * self.n
        self.cdparent = [-1] * self.n
        self.cddepth = [0] * self.n
        self.cdorder = [-1] * self.n
        self.cdused = [0] * self.n
 
        cnt = 0
        stack = [0]
        while stack:
            v = stack.pop()
            p = self.cdparent[v]
            c = self.get_centroid(v)
            self.cdused[c] = True
            self.cdparent[c] = p
            self.cddepth[c] = self.cddepth[v]
            self.cdorder[c] = cnt
            cnt += 1
            for u in self.graph[c]:
                if self.cdused[u]:
                    continue
                self.cdparent[u] = c
                self.cddepth[u] = self.cddepth[c]+1
                stack.append(u)
 
    def get_centroid(self, root):
        self.parent[root] = -1
        self.subtree[root] = 1
        stack = [root]
        order = []
        while stack:
            v = stack.pop()
            order.append(v)
            for u in graph[v]:
                if self.parent[v] == u or self.cdused[u]:
                    continue
                self.subtree[u] = 1
                self.parent[u] = v
                stack.append(u)
        if len(order) <= 2:
            return root
        for v in reversed(order):
            if self.parent[v] == -1:
                continue
            self.subtree[self.parent[v]] += self.subtree[v]
        total = self.subtree[root]
        v = root
        while True:
            for u in self.graph[v]:
                if self.parent[v] == u or self.cdused[u]:
                    continue
                if self.subtree[u] > total // 2:
                    v = u
                    break
            else:
                return v
 
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
 
n, q = map(int,input().split())
graph = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = [int(x) - 1 for x in input().split()]
    graph[u].append(v)
    graph[v].append(u)
 
prev = [0] * n
depth = [0] * n
Q = [0]
while Q:
    v = Q.pop()
    for u in graph[v]:
        if u != prev[v]:
            prev[u] = v
            depth[u] = depth[v] + 1
            Q.append(u)
 
LOG = n.bit_length()
up = [[0] * LOG for _ in range(n)]
for node in range(1, n):
    up[node][0] = prev[node]
for k in range(1, LOG):
    for node in range(1, n):
        up[node][k] = up[up[node][k - 1]][k - 1]
 
min_dist = [0] * n
for v in range(n):
    min_dist[v] = depth[v]
 
cd = CentroidDecomposition(graph)
 
for _ in range(q):
    t, v = [int(x) - 1 for x in input().split()]
    if t == 0:
        cur = v
        while cur != -1:
            lca = get_lca(cur, v)
            dist = depth[cur] + depth[v] - 2 * depth[lca]
            min_dist[cur] = min(min_dist[cur], dist)
            cur = cd.cdparent[cur]
    else:
        ans = n
        cur = v
        while cur != -1:
            lca = get_lca(cur, v)
            dist = depth[cur] + depth[v] - 2 * depth[lca]
            ans = min(ans, dist + min_dist[cur])
            cur = cd.cdparent[cur]
        print(ans)