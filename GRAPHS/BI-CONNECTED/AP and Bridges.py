def cut_nodes_edges(graph):
    n = len(graph)
    t = 0
    num = [None] * n
    low = [n] * n
    p = [None] * n
    ch = [0] * n
    ts = [-1] * n
    for start in range(n):
        if ts[start] == -1:
            ts[start] = 0
            Q = [start]
            while Q:
                v = Q[-1]
                if ts[v] == 0:
                    num[v] = t
                    t += 1
                    #low[v] = float('inf')
                if ts[v] == len(graph[v]):
                    Q.pop()
                    up = p[v]
                    if up is not None:
                        low[up] = min(low[up], low[v])
                        if low[v] >= num[up]:
                            ch[up] += 1
                else:
                    u = graph[v][ts[v]]
                    ts[v] += 1
                    if ts[u] == -1:
                        p[u], ts[u] = v, 0
                        Q.append(u)
                    elif num[u] < num[v] and p[v] != u:
                        low[v] = min(low[v], num[u])
    cut_edges = []
    cut_nodes = []
    for v in range(n):
        if p[v] == None:
            if ch[v] >= 2: cut_nodes.append(v)
        else:
            if ch[v] >= 1: cut_nodes.append(v)
            if low[v] >= num[v]: cut_edges.append((p[v], v))
    return cut_nodes, cut_edges


if __name__=="__main__":

    n, m = map(int,input().split())
    graph = [[] for _ in range(n)]
    for _ in range(m):
        a,b = map(int,input().split())
        graph[a-1].append(b-1)
        graph[b-1].append(a-1)
    
    print(*cut_nodes_edges(graph),sep='\n')