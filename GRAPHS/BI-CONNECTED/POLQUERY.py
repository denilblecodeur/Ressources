from sys import stdin, stdout

def main():
    def cut_nodes_edges(graph):
        n = len(graph)
        time = 0
        num = [None] * n
        low = [n] * n
        father = [None] * n
        critical_childs = [0] * n
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
                        low[node] = float('inf')
                    children = graph[node]
                    if times_seen[node] == len(children):
                        to_visit.pop()
                        up = father[node]
                        if up is not None:
                            low[up] = min(low[up], low[node])
                            if low[node] >= num[up]:
                                critical_childs[up] += 1
                    else:
                        child = children[times_seen[node]]
                        times_seen[node] += 1
                        if times_seen[child] == -1:
                            father[child] = node
                            times_seen[child] = 0
                            to_visit.append(child)
                        elif num[child] < num[node] and father[node] != child:
                            low[node] = min(low[node], num[child])
        cut_edges = []
        cut_nodes = []
        for node in range(n):
            if father[node] == None:
                if critical_childs[node] >= 2:
                    cut_nodes.append(node)
            else:
                if critical_childs[node] >= 1:
                    cut_nodes.append(node)
                if low[node] >= num[node]:
                    cut_edges.append(sorted((father[node], node)))
        return cut_nodes, cut_edges

    def dfs(start, target, removed_edge):
        visited = [False] * N
        to_visit = [start]
        while to_visit:
            node = to_visit.pop()
            if not visited[node]:
                visited[node] = True
                if node == target:
                    return True
                for neigh in graph[node]:
                    if not (node in removed_edge and neigh in removed_edge):
                        to_visit.append(neigh)
        return False
    
    def dfs(start, target, removed_node):
        visited = [False] * N
        to_visit = [start]
        while to_visit:
            node = to_visit.pop()
            if node != removed_node and not visited[node]:
                visited[node] = True
                if node == target:
                    return True
                for neigh in graph[node]:
                    to_visit.append(neigh)
        return False

    N, E = map(int,stdin.readline().split())
    graph = [[] for _ in range(N)]
    for _ in range(E):
        a, b = map(int,stdin.readline().split())
        graph[a - 1].append(b - 1)
        graph[b - 1].append(a - 1)

    cut_nodes, cut_edges = cut_nodes_edges(graph)

    stdin.readline()
    for line in stdin:
        if line[0] == '1':
            _, a, b, g1, g2 = map(int,line.split())
            removed_edge = sorted((g1 - 1, g2 - 1))
            if removed_edge not in cut_edges or dfs(a - 1, b - 1, removed_edge):
                stdout.write('da\n')
            else:
                stdout.write('ne\n')
        else:
            _, a, b, c = map(int,line.split())
            removed_node = c - 1
            if removed_node not in cut_nodes or dfs(a - 1, b - 1, removed_node):
                stdout.write('da\n')
            else:
                stdout.write('ne\n')
main()