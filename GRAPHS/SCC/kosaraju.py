def kosaraju_dfs(graph, nodes, order, sccp):
    times_seen = [-1] * len(graph)
    for start in nodes:
        if times_seen[start] == -1:
            to_visit = [start]
            times_seen[start] = 0
            sccp.append([start + 1])
            while to_visit:
                node = to_visit[-1]
                children = graph[node]
                if times_seen[node] == len(children):
                    to_visit.pop()
                    order.append(node)
                else:
                    child = children[times_seen[node]]
                    times_seen[node] += 1
                    if times_seen[child] == -1:
                        times_seen[child] = 0
                        to_visit.append(child)
                        sccp[-1].append(child + 1)

def reverse(graph):
    rev_graph = [[] for node in graph]
    for node in range(len(graph)):
        for neighbor in graph[node]:
            rev_graph[neighbor].append(node)
    return rev_graph

def kosaraju(graph):
    n = len(graph)
    order = []
    sccp = []
    kosaraju_dfs(graph, range(n), order, [])
    kosaraju_dfs(reverse(graph), order[::-1], [], sccp)
    return sccp[::-1]

if __name__=="__main__":

    n, m = map(int,input().split())
    graph = [[] for _ in range(n)]
    for _ in range(m):
        a,b = map(int,input().split())
        graph[a-1].append(b-1)
    
    print(kosaraju(graph))