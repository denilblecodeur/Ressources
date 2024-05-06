#Maximum flow - Ford-Fulkerson O(V * E * Capa_max)

def get_maxflow(adj, capacity, s, t):
    n = len(adj)
    par = [-1] * n
    def augment():
        for i in range(n):
            par[i] = -1
        par[s] = -2
        q = [(s, 1<<59)]
        while len(q) > 0:
            x, flow = q.pop()
            for y in adj[x]:
                if par[y] == -1 and capacity[x][y] > 0:
                    par[y] = x
                    new_flow = min(flow, capacity[x][y])
                    if y == t:
                        return new_flow
                    q.append((y, new_flow))
        return 0
    flow = 0
    while True:
        flow_delta = augment()
        if flow_delta == 0:
            break
        flow += flow_delta
        x = t
        while x != s:
            p = par[x]
            capacity[p][x] -= flow_delta
            capacity[x][p] += flow_delta
            x = p
    return flow

# Short code #################################
# + fonctionne si arcs bidirectionnels à capacité partagée

def augment(graph, capacity, flow, val, u, target, visit):
    visit[u] = True
    if u == target:
        return val
    for v in graph[u]:
        cuv = capacity[u][v]
        if not visit[v] and cuv > flow[u][v]:
            res = min(val, cuv - flow[u][v])
            delta = augment(graph, capacity, flow, res, v, target, visit)
            if delta > 0:
                flow[u][v] += delta
                flow[v][u] -= delta
                return delta
    return 0

def ford_fulkerson(graph, capacity, s, t):
    # Capacités doivent être entières
    # capacity matrice, si arc (u -> v) existe,
    # (v -> u) doit exister (capa 0 si nécessaire, sinon même que (u -> v)
    add_reverse_arcs(graph, capacity)
    n = len(graph)
    flow = [[0] * n for _ in range(n)]
    INF = 1<<59
    while augment(graph, capacity, flow, INF, s, t, [False] * n) > 0:
        pass
    return flow, sum(flow[s])     # flot, valeur du flot


# Alternative #################################

# Ne fonctionne pas si arcs bidirectionnels à capacité partagée
n, m = map(int, input().split())
graph = [{} for _ in range(n)]
for _ in range(m):
    u, v, c = map(int,input().split())
    u -= 1; v -= 1
    if u not in graph[v]: graph[v][u] = 0
    if v not in graph[u]: graph[u][v] = 0
    graph[v][u] += c
    graph[u][v] += c
 
def bfs(graph):
    n = len(graph)
    Q = deque([0])
    prev = [-1] * n
    visited = [False] * n
    while Q:
        node = Q.popleft()
        visited[node] = True
        if node == n - 1:
            break
        for neighbor in graph[node]:
            if not visited[neighbor]:
                prev[neighbor] = node
                Q.append(neighbor)
    if not visited[-1]:
        return None
    path = []
    current = n - 1
    while current != 0:
        path.append(current)
        current = prev[current]
    return path[::-1]
 
total = 0
while True:
    path = bfs(graph)
    if path is None:
        break
    flow = 1<<59
    current = 0
    for step in path:
        flow = min(flow, graph[current][step])
        current = step
    current = 0
    for step in path:
        graph[current][step] -= flow
        if graph[current][step] == 0:
            del graph[current][step]
        if current not in graph[step]:
            graph[step][current] = 0
        graph[step][current] += flow
        current = step
    total += flow
    
print(total)

# Just to remind
def add_reverse_arcs(graph, capac=None):
    """Utility function for flow algorithms that need for every arc (u,v),
    the existence of an (v,u) arc, by default with zero capacity.
    graph can be in adjacency list, possibly with capacity matrix capac.
    or graph can be in adjacency dictionary, then capac parameter is ignored.

    :param capac: arc capacity matrix
    :param graph: in listlist representation, or in listdict representation,
        in this case capac is ignored
    :complexity: linear
    :returns: nothing, but graph is modified
    """
    for u, _ in enumerate(graph):
        for v in graph[u]:
            if u not in graph[v]:
                if type(graph[v]) is list:
                    graph[v].append(u)
                    if capac:
                        capac[v][u] = 0
                else:
                    assert type(graph[v]) is dict
                    graph[v][u] = 0