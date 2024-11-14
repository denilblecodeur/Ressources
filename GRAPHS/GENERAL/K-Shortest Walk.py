"""
Problem Description:
- You are given a directed graph with N vertices and M edges.
- Each edge i is directed from vertex a_i to vertex b_i and has a weight c_i.
- The graph may contain multiple edges between two vertices or self-loops.

Objective:
- Given a start vertex `s` and an end vertex `t`, output the lengths of the K shortest walks from vertex `s` to vertex `t`.
- For each `i` from 1 to K, let x_i be the length of the i-th shortest walk from `s` to `t`.
- If there are fewer than K distinct walks from `s` to `t`, output -1 for the remaining values.
- Note: Multiple walks with the same length are considered different walks.

Constraints:
- 1 ≤ N, M ≤ 300,000
- 1 ≤ K ≤ 300,000
- 0 ≤ s, t < N
- 0 ≤ u_i, v_i < N
- 0 ≤ c_i ≤ 10^7
"""

from heapq import *
class LefitistHeap:
    def __init__(self, rank: int, key: int, value: int, left: int, right: int):
        self.rank = rank
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    @staticmethod
    def insert(a: "LefitistHeap", key: int, value: int):
        if not a or key < a.key:
            return LefitistHeap(1, key, value, a, None)
        l, r = a.left, LefitistHeap.insert(a.right, key, value)
        if not l or r.rank > l.rank:
            l, r = r, l
        return LefitistHeap((r.rank if r else 0) + 1, a.key, a.value, l, r)

    def __lt__(self, _):
        return False

def dijkstra(graph: list[list[int]], start: int) -> tuple[list[int], list[int]]:
    INF = float("inf")
    n = len(graph)
    dist = [INF] * n
    dist[start] = 0
    prev = [-1] * n

    que = [(0, start)]  # 距離,頂点
    while que:
        c, u = heappop(que)
        if c > dist[u]:
            continue
        for nc, v in graph[u]:
            cost = dist[u] + nc
            if cost < dist[v]:
                dist[v] = cost
                prev[v] = u
                heappush(que, (cost, v))

    return dist, prev


def shortest_paths(n: int, edges: list[tuple[int, int, int]], s: int, t: int, k: int):
    adj = [[] for _ in range(n)]
    adj_rev = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((w, v))
        adj_rev[v].append((w, u))
    inf = float("inf")
    dist, prev = dijkstra(adj_rev, t)
    if dist[s] == inf:
        return []

    g = [[] for _ in range(n)]
    for u in range(n):
        if prev[u] != -1:
            g[prev[u]].append(u)

    h = [None] * n
    q = [t]
    for u in q:
        seen = False
        for w, v in adj[u]:
            if dist[v] == inf:
                continue
            c = w + dist[v] - dist[u]
            if not seen and v == prev[u] and c == 0:
                seen = True
                continue
            h[u] = LefitistHeap.insert(h[u], c, v)
        for v in g[u]:
            h[v] = h[u]
            q.append(v)

    ans = [dist[s]]
    if not h[s]:
        return ans

    q = [(dist[s] + h[s].key, h[s])]
    while q and len(ans) < k:
        cd, ch = heappop(q)
        ans.append(cd)
        if h[ch.value]:
            heappush(q, (cd + h[ch.value].key, h[ch.value]))
        if ch.left:
            heappush(q, (cd + ch.left.key - ch.key, ch.left))
        if ch.right:
            heappush(q, (cd + ch.right.key - ch.key, ch.right))
    return ans


n, m, s, t, k = map(int, input().split())
es = [tuple(map(int,input().split())) for _ in range(m)]
ans = shortest_paths(n, es, s, t, k)
while len(ans) < k:
    ans.append(-1)
print(*ans, sep="\n")    