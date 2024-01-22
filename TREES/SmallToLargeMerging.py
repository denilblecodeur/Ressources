import sys
input = sys.stdin.buffer.readline

def merge(u, v):
    if len(colors[u]) < len(colors[v]):
        colors[v], colors[u] = colors[u], colors[v]
        _sum[v], _sum[u] = _sum[u], _sum[v]
        mx[v], mx[u] = mx[u], mx[v]
    for c, value in colors[v].items():
        if c not in colors[u]:
            colors[u][c] = 0
        colors[u][c] += value
        if colors[u][c] > mx[u]:
            mx[u] = colors[u][c]
            _sum[u] = c
        elif colors[u][c] == mx[u]:
            _sum[u] += c

n = int(input())
_sum = list(map(int,input().split()))
mx = [1] * n
colors = [{c:1} for c in _sum]
adj = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = [int(x) - 1 for x in input().split()]
    adj[u].append(v)
    adj[v].append(u)

ans = [0] * n
prev = [0] * n
time_seen = [-1] * n
time_seen[0] = 0
Q = [0]
while Q:
    u = Q[-1]
    if time_seen[u] == len(adj[u]):
        ans[u] = _sum[u]
        merge(prev[u], u)
        Q.pop()
    else:
        v = adj[u][time_seen[u]]
        if v == prev[u]:
            time_seen[u] += 1
            if time_seen[u] == len(adj[u]):
                continue
            v = adj[u][time_seen[u]]
        prev[v] = u
        time_seen[u] += 1
        time_seen[v] = 0
        Q.append(v)

print(*ans)