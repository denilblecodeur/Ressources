class BiconnectedComponents:
    def __init__(self, graph):
        self.n = n = len(graph)
        self.m = sum(len(dsts) for dsts in graph) >> 1
        self.num_bcs = 0
        self.graph = graph
        self.bc_vertex_pair = []
        if n == 0:
            self.num_bcs = 0
            return
        used = bytearray(n)
        parent = [0] * n
        order = [0] * n
        def dfs(start, idx):
            stack = [start]
            parent[start] = -1
            while stack:
                cur = stack.pop()
                if used[cur]: continue
                used[cur] = 1
                order[idx] = cur
                idx += 1
                for dst in graph[cur]:
                    if not used[dst]:
                        parent[dst] = cur
                        stack.append(dst)
            return idx
        idx = 0
        for s in range(n):
            if not used[s]:
                idx = dfs(s, idx)
        vertex_to_dfs = [0] * n
        for i in range(n): vertex_to_dfs[order[i]] = i
        low = vertex_to_dfs[:]

        for p in range(n):
            for e in graph[p]:
                low[p] = min(low[p], vertex_to_dfs[e])

        for i in reversed(range(n)):
            p = order[i]
            pp = parent[p]
            if pp >= 0:
                low[pp] = min(low[pp], low[p])

        num_bcs = 0
        for p in order:
            if parent[p] < 0: continue
            pp = parent[p]
            if low[p] < vertex_to_dfs[pp]:
                low[p] = low[pp]
                self.bc_vertex_pair.append((low[p], p))
            else:
                low[p] = num_bcs
                num_bcs += 1
                self.bc_vertex_pair.append((low[p], pp))
                self.bc_vertex_pair.append((low[p], p))

        for s in range(n):
            if not graph[s]:
                self.bc_vertex_pair.append((num_bcs, s))
                num_bcs += 1
        self.num_bcs = num_bcs

    def __len__(self):
        return self.num_bcs

    def bcc(self):
        bcc_ = [[] for _ in range(self.num_bcs)]
        for idx, v in self.bc_vertex_pair:
            bcc_[idx].append(v)
        return bcc_
    
    # get merged bccs, to transform the graph to a tree
    def merged_bcc(self):
        bcc_ = []
        repr_ = [-1] * self.n
        N = 0
        for vertex_list in self.bcc():
            if len(vertex_list) <= 2:
                continue
            to_merge = []
            for v in vertex_list:
                if repr_[v] == -1:
                    repr_[v] = N
                else:
                    to_merge.append(repr_[v])
            if to_merge == []:
                bcc_.append(vertex_list)
                N += 1
            else:
                main = min(to_merge)
                for v in vertex_list:
                    repr_[v] = main
                for i in to_merge:
                    for v in bcc_[i]:
                        repr_[v] = main
        BCCs = [[] for _ in range(N)]
        for v in range(self.n):
            if repr_[v] == -1:
                repr_[v] = N
                BCCs.append([v])
                N += 1
            else:
                BCCs[repr_[v]].append(v)
        return BCCs, repr_


n, m = map(int,input().split())
graph = [[] for _ in range(n)]
for _ in range(m):
    a, b = map(int,input().split())
    graph[a].append(b)
    graph[b].append(a)
BC = BiconnectedComponents(graph)
print(len(BC))
for bcc in BC.bcc():
    print(len(bcc), *bcc)