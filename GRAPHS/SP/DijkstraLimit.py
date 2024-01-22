def dijkstra(src, dest, graph, limit):
    heap = [(0, 0, src)]
    distances = {src: {0: 0}}
    while heap:
        current_cost, current_dist, node = heappop(heap)
        if node == dest:
            return current_cost
        for cost_n, dist_n, neigh in graph[node]:
            newdist = current_dist + dist_n
            newcost = current_cost + cost_n
            if newdist <= limit:
                if neigh not in distances:
                    distances[neigh] = {}
                if newdist not in distances[neigh] or distances[neigh][newdist] > newcost:
                    distances[neigh][newdist] = newcost 
                    heappush(heap, (newcost, newdist, neigh))
    return -1