# calculate something on the path from a to b

# FAST CLASS HLD + LCA
class HLD:
    def __init__(self, E, root=0):
        self.E = E
        self.root = root
        self.N = N = len(E)
        self.Parent = [-1] * N
        self.Size = [-1] * N
        self.dfs1()

        self.Mapping = [-1] * N
        self.Head = list(range(N))
        self.Depth = [0] * N
        self.dfs2()

        ### to comment if not necessary
        self.NLOG = 1 << N.bit_length()
        self.Seg = [0] * (2 * self.NLOG)
        self.TreePos = [0] * N
        self.fill()
        ###

    def dfs1(self):
        E = self.E
        Parent, Size = self.Parent, self.Size
        Path = [self.root]
        Idx_edge = [0]
        while Path:
            v = Path[-1]
            idx_edge = Idx_edge[-1]
            Ev = E[v]
            if idx_edge != len(Ev):
                u = Ev[idx_edge]
                Idx_edge[-1] += 1
                E[u].remove(v)
                Parent[u] = v
                Path.append(u)
                Idx_edge.append(0)
            else:
                if len(Ev) >= 2:
                    ma = -1
                    argmax = None
                    for i, u in enumerate(Ev):
                        if Size[u] > ma:
                            ma = Size[u]
                            argmax = i
                    u0, um = Ev[0], Ev[argmax]
                    Size[u0], Size[um] = Size[um], Size[u0]
                    Ev[0], Ev[argmax] = Ev[argmax], Ev[0]
                Size[v] = sum(Size[u] for u in Ev) + 1
                Path.pop()
                Idx_edge.pop()
    
    def dfs2(self):
        E = self.E
        Mapping = self.Mapping
        Head = self.Head
        Depth = self.Depth
        k = 0
        St = [self.root]
        while St:
            v = St.pop()
            Mapping[v] = k
            k += 1
            Ev = E[v]
            if Ev:
                Head[Ev[0]] = Head[v]
                St += Ev[::-1]
                for u in Ev:
                    Depth[u] = Depth[v] + 1
    
    def lca(self, v, u):
        Parent = self.Parent
        Mapping = self.Mapping
        Head = self.Head
        while True:
            if Mapping[v] > Mapping[u]:
                v, u = u, v
            if Head[v] == Head[u]:
                return v
            u = Parent[Head[u]]
    
    def distance(self, v, u):
        Depth = self.Depth
        return Depth[v] + Depth[u] - 2 * Depth[self.lca(v, u)]
    
    def update(self, p, val):
        Seg = self.Seg
        p += self.NLOG
        Seg[p] = val
        while p > 1:
            Seg[p>>1] = max(Seg[p], Seg[p^1])
            p >>= 1

    def query(self, l, r): # [l, r)
        Seg = self.Seg
        res = -1
        l += self.NLOG; r += self.NLOG
        while l < r:
            if l&1: res = max(res, Seg[l]); l += 1
            if r&1: r -= 1; res = max(res, Seg[r])
            l >>= 1; r >>= 1
        return res
    
    def fill(self):
        E = self.E
        NLOG = self.NLOG
        Seg = self.Seg
        Parent = self.Parent
        TreePos = self.TreePos
        currentPos = 0
        for i in range(self.N):
            if Parent[i] == -1 or E[Parent[i]][0] != i:
                j = i
                while j != -1:
                    TreePos[j] = currentPos
                    Seg[NLOG + currentPos] = val[j] #TO CHANGE
                    currentPos += 1
                    j = E[j][0] if len(E[j]) else -1
        for k in range(NLOG - 1, 0, -1):
            Seg[k] = max(Seg[k<<1], Seg[k<<1|1])
    
    def path(self, u, v):
        Parent = self.Parent
        Depth = self.Depth
        Head = self.Head
        TreePos = self.TreePos
        res = -1
        while Head[v] != Head[u]:
            if Depth[Head[v]] > Depth[Head[u]]:
                v, u = u, v
            res = max(res, self.query(TreePos[Head[u]], TreePos[u] + 1))
            u = Parent[Head[u]]
        if Depth[u] > Depth[v]:
            v, u = u, v
        res = max(res, self.query(TreePos[u], TreePos[v] + 1))
        return res



# ANOTHER CODE THAT WORK

def update(p, val):
    p += N
    seg[p] = val
    while p > 1:
        seg[p>>1] = max(seg[p], seg[p^1])
        p >>= 1

def query(l, r): # [l, r)
    res = -1
    l += N; r += N
    while l < r:
        if l&1: res = max(res, seg[l]); l += 1
        if r&1: r -= 1; res = max(res, seg[r])
        l >>= 1; r >>= 1
    return res

n, q = map(int,input().split())
val = list(map(int,input().split()))
adj = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = [int(x) - 1 for x in input().split()]
    adj[u].append(v)
    adj[v].append(u)

parent = [0] * n
heavy = [-1] * n
depth = [0] * n
subtree = [1] * n
time_seen = [-1] * n
time_seen[0] = 0
Q = [0]
while Q:
    u = Q[-1]
    if time_seen[u] == len(adj[u]):
        maxSubtree = 0
        for v in adj[u]:
            if v != parent[u]:
                subtree[u] += subtree[v]
                if subtree[v] > maxSubtree:
                    maxSubtree = subtree[v]
                    heavy[u] = v
        Q.pop()
    else:
        v = adj[u][time_seen[u]]
        if v == parent[u]:
            time_seen[u] += 1
            if time_seen[u] == len(adj[u]):
                continue
            v = adj[u][time_seen[u]]
        parent[v] = u
        depth[v] = depth[u] + 1
        Q.append(v)
        time_seen[u] += 1
        time_seen[v] = 0

N = 1 << n.bit_length()
seg = [0] * (2 * N)
root = [0] * n
treePos = [0] * n
currentPos = 0
for i in range(n):
    if heavy[parent[i]] != i:
        j = i
        while j != -1:
            root[j] = i
            treePos[j] = currentPos
            seg[N + currentPos] = val[j]
            currentPos += 1
            j = heavy[j]
for k in range(N - 1, 0, -1):
    seg[k] = max(seg[k<<1], seg[k<<1|1])

def path(u, v):
    ret = 0
    while root[u] != root[v]:
        if depth[root[u]] < depth[root[v]]:
            u, v = v, u
        ret = max(ret, query(treePos[root[u]], treePos[u] + 1))
        u = parent[root[u]]
    if depth[u] > depth[v]:
        u, v = v, u
    ret = max(ret, query(treePos[u], treePos[v] + 1))
    return ret

ans = []
for _ in range(q):
    typ, u, v = map(int,input().split())
    if typ == 1:
        val[u - 1] = v
        update(treePos[u - 1], v)
    else:
        res = path(u - 1, v - 1)
        ans.append(res)
print(*ans)