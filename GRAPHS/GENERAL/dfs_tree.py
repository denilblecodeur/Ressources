if cut_nodes_edges(g):
    print(0) & exit()

ans = [set() for _ in range(n)]
seen = [False] * n
seen[0] = True
d = [-1] * n

@bootstrap
def dfs(p, v):
    d[v] = d[p]+1
    for u in g[v]:
        if u == p:
            continue
        if seen[u]:
            # back edge
            if d[v] < d[u]:
                ans[u].add(v)
            else:
                ans[v].add(u)
        else:
            seen[u] = True
            ans[v].add(u)  # dfs tree edge
            (yield dfs(v, u))
    yield

dfs(0, 0)
for v in range(n):
    for u in ans[v]:
        print(v+1, u+1)
