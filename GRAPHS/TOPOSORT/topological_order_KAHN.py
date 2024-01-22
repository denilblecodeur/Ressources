#w/o priority
def topological_order(graph, indeg):
    Q = [node for node in range(len(graph)) if indeg[node] == 0]
    order = []
    while Q:
        node = Q.pop()
        order.append(node + 1)
        for neighbor in graph[node]:
            indeg[neighbor] -= 1
            if indeg[neighbor] == 0:
                Q.append(neighbor)
    return order

#with priority
from heapq import heappush, heappop, heapify
def topological_order(graph, indeg):
    Q = [node for node in range(len(graph)) if indeg[node] == 0]
    order = []
    while Q:
        node = heappop(Q)
        order.append(node + 1)
        for neigh in graph[node]:
            indeg[neigh] -= 1
            if indeg[neigh] == 0:
                heappush(Q, neigh)
    return order

#smallest perm
revgraph = [[] for _ in range(n)]
outdeg = [0] * n
for _ in range(m):
    a, b = map(int,input().split())
    revgraph[b - 1].append(a - 1)
    outdeg[a - 1] += 1
Q = [-node for node in range(n) if outdeg[node] == 0]
heapify(Q)
order = []
while Q:
    node = -heappop(Q)
    order.append(node + 1)
    for neigh in revgraph[node]:
        outdeg[neigh] -= 1
        if outdeg[neigh] == 0:
            heappush(Q, -neigh)
print(*order[::-1])