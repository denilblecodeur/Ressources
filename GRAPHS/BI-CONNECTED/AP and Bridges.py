def cut_nodes_edges(graph):
    n = len(graph)
    time = 0
    num = [None] * n
    low = [n] * n
    parent = [None] * n         # parent[v] = père de v, None si racine
    critical_childs = [0] * n   #c_childs[u] = nb fils v tq low[v] >= num[u]
    times_seen = [-1] * n
    for start in range(n):
        if times_seen[start] == -1:
            times_seen[start] = 0
            to_visit = [start]
            while to_visit:
                node = to_visit[-1]
                if times_seen[node] == 0:
                    num[node] = time
                    time += 1
                    #low[node] = float('inf')
                children = graph[node]
                if times_seen[node] == len(children):   #fin traitement
                    to_visit.pop()
                    up = parent[node]             # propager low au père
                    if up is not None:
                        low[up] = min(low[up], low[node])
                        if low[node] >= num[up]:
                            critical_childs[up] += 1
                else:
                    child = children[times_seen[node]]     # prochain arc
                    times_seen[node] += 1
                    if times_seen[child] == -1:     # pas encore visité
                        parent[child] = node        # arc de liaison
                        times_seen[child] = 0
                        to_visit.append(child)      # (dessous) arc retour
                    elif num[child] < num[node] and parent[node] != child:
                        low[node] = min(low[node], num[child])
    cut_edges = []
    cut_nodes = []
    for node in range(n):
        if parent[node] == None:
            if critical_childs[node] >= 2:
                cut_nodes.append(node)
        else:
            if critical_childs[node] >= 1:
                cut_nodes.append(node)
            if low[node] >= num[node]:
                cut_edges.append((parent[node], node))
    return cut_nodes, cut_edges


if __name__=="__main__":

    n, m = map(int,input().split())
    graph = [[] for _ in range(n)]
    for _ in range(m):
        a,b = map(int,input().split())
        graph[a-1].append(b-1)
        graph[b-1].append(a-1)
    
    print(*cut_nodes_edges(graph),sep='\n')