from sys import stdin, stdout

def main():
    def kosaraju_dfs(graph, nodes, order, sccp):
        times_seen = [-1] * len(graph)
        for start in nodes:
            if times_seen[start] == -1:
                to_visit = [start]
                times_seen[start] = 0
                sccp.append([start])
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
                            sccp[-1].append(child)
    def reverse(graph):
        n = len(graph)
        rev_graph = [[] for _ in range(n)]
        for node in range(n):
            for neigh in graph[node]:
                rev_graph[neigh].append(node)
        return rev_graph

    def kosaraju(graph):
        n = len(graph)
        order = []
        sccp = []
        kosaraju_dfs(graph, range(n), order, [])
        kosaraju_dfs(reverse(graph), order[::-1], [], sccp)
        return sccp[::-1]

    def _vertex(lit):
        if lit > 0:
            return 2 * (lit - 1)
        else:
            return 2 * (-lit - 1) + 1
    
    def two_sat(formula):
        n = max(abs(clause[p]) for p in (0, 1) for clause in formula)
        graph = [[] for _ in range(2 * n)]
        for x, y in formula:
            graph[_vertex(-x)].append(_vertex(y))
            graph[_vertex(-y)].append(_vertex(x))
        sccp = kosaraju(graph)
        comp_id = [None] * (2 * n)
        affectations = [None] * (2 * n)
        for component in sccp:
            rep = min(component)
            for vtx in component:
                comp_id[vtx] = rep
                if affectations[vtx] == None:
                    affectations[vtx] = True
                    affectations[vtx ^ 1] = False
        for i in range(n):
            if comp_id[2 * i] == comp_id[2 * i + 1]:
                return None
        return affectations[::2]

    for _ in range(int(stdin.readline())):
        A, S, m = map(int,stdin.readline().split())
        formula = []
        for _ in range(m):
            s1, a1, s2, a2 = map(int,stdin.readline().split())
            s1 += A
            s2 += A
            if a2 < a1:
                s2 *= -1
                s1 *= -1
            if s2 < s1:
                a2 *= -1
                a1 *= -1
            formula.extend([(s1, s2), (s1, a2), (a1, s2), (a1, a2)])
        affectations = two_sat(formula)
        print('YES' if affectations else 'NO')

main()