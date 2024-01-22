# Minimum vertex cover
# MCBM = MVC = V - MIS

n, m = len(even), len(odd)
bm = BipartiteMatching(n, m)
edges = []
for i, e in enumerate(even):
    for j, o in enumerate(odd):
        if spf[e + o] == -1:
            bm.add_edge(i, j)
            edges.append((i, j))

matching = bm.solve()

graph = [{} for _ in range(n + m)]
unmatched_left = [True] * n
# left side : 0 to n - 1
# right side : n to n + m - 1
for e, o in matching:
    # matched edges start from the right side of the graph to the left side
    unmatched_left[e] = False
    graph[o + n][e] = 1
    graph[e][o + n] = -1
# free edges start from the left side of the graph to the right side
for e, o in edges:
    if o + n not in graph[e]:
        graph[e][o + n] = 1
        graph[o + n][e] = -1
# Run DFS from unmatched nodes of the left side,
# in this traversal some nodes will become visited, others will stay unvisited.
vis = [False] * (n + m)
for e in range(n):
    if unmatched_left[e]:
        Q = [e]
        while Q:
            v = Q.pop()
            vis[v] = True
            for u, w in graph[v].items():
                if w == 1 and not vis[u]:
                    Q.append(u)
# The MVC nodes are the visited nodes from the right side, and unvisited nodes from the left side.
MVC = []
for e in range(n):
    if not vis[e]:
        MVC.append(even[e])
for o in range(n, n + m):
    if vis[o]:
        MVC.append(odd[o - n])
print(len(MVC))
print(*MVC)