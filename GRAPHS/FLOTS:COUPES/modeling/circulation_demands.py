"""
Circulation with d(e) <= f(e) <= c(e)
FranceIOI : Nouvelle attraction
"""

def add_edge(G, a, b, c):
    if a not in G[b]:
        G[a][b] = G[b][a] = 0
    G[a][b] += c

N, M = map(int,input().split())
graph = [{} for _ in range(N+2)]
isum, osum = [0]*N, [0]*N
edges = []
for _ in range(M):
    a, b, d, c = map(int,input().split())
    a-= 1; b -= 1
    add_edge(graph, a, b, c-d)
    isum[b]+=d
    osum[a]+=d
s, t = N, N+1
indemands = outdemands = 0
for v in range(N):
    need = isum[v] - osum[v]
    if need < 0:
        add_edge(graph, v, t, -need)
        outdemands -= need
    if need > 0:
        add_edge(graph, s, v, need)
        indemands += need
if indemands != outdemands:
    print("NON")
else:
    _, mf = dinic(s, t, graph)
    print("OUI" if mf == indemands else "NON")