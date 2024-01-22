def eulerian_tour_undirected(n, m, graph):
    Q = [0]
    path = []
    while Q:
        node = Q[-1]
        visited[node] = True        #See prequisites below
        if len(graph[node]) == 0:
            path.append(Q.pop())
            continue
        neigh = graph[node].pop()
        graph[neigh].remove(node)   # Graph is list of sets
        Q.append(neigh)
    return path if len(path) == m + 1 else -1

#Fleury’s Algorithm (fonctionne avec multigraph)
def get_eulerian_tour(edges, src): # edges is a matrix
    def get_next_node(node):
        current, degree = 0, 0
        for neigh, deg in enumerate(edges[node]):
            if deg > degree:
                current, degree = neigh, deg
        if degree > 0:
            edges[node][current] -= 1
            edges[current][node] -= 1
            return (node, current)
        else:
            return None
    _next = get_next_node(src[1])
    order = deque([_next])
    blocked = 0
    while blocked < n:
        _next = get_next_node(order[-1][1])
        if _next:
            order.append(_next)
            blocked = 0
        elif len(order) != n:
            prev = order.pop()
            order.appendleft(prev)
            blocked += 1
        else:
            break
    return order if len(order) == n else None # ou n+1?

#Prequisites:
N, A = map(int,input().split())
graph = [set() for _ in range(N)]
visited = [True] * N
even_degree = 0
for _ in range(A):
    a, b = map(int,input().split())
    graph[a - 1].add(b - 1)
    graph[b - 1].add(a - 1)
    even_degree ^= (1 << (a - 1)) ^ (1 << (b - 1))
    visited[a - 1] = visited[b - 1] = False
if even_degree == 0:
    euler_tour = circuit(N, A, graph)
    if all(visited):
        return euler_tour
return -1