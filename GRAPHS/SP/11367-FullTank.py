from sys import stdin, stdout
input = stdin.buffer.readline
from heapq import heappush, heappop

def main():
    def dijkstra(start, target, cap):
        dp = [[-1] * (cap + 1) for _ in range(n)]
        heap = [(0, 0, start)]
        while heap:
            current_cost, fuel, city = heappop(heap)
            if city == target:
                return str(current_cost)
            for next_city in graph[city]:
                length = weight[city][next_city]
                if fuel - length >= 0:
                    newfuel = fuel - length
                    if dp[next_city][newfuel] == -1 or dp[next_city][newfuel] > current_cost:
                        dp[next_city][newfuel] = current_cost
                        heappush(heap, (current_cost, newfuel, next_city))
            for unit_fuel in range(1, cap - fuel + 1):
                newcost = current_cost + fuel_price[city] * unit_fuel
                newfuel = fuel + unit_fuel
                if dp[city][newfuel] == -1 or dp[city][newfuel] > newcost:
                    dp[city][newfuel] = newcost
                    heappush(heap, (newcost, newfuel, city))
        return 'impossible'

    n, m = map(int, input().split())
    fuel_price = list(map(int, input().split()))
    graph = [[] for _ in range(n)]
    weight = [[-1] * n for _ in range(n)]
    for _ in range(m):
        a, b, c = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)
        if weight[a][b] == -1 or c < weight[a][b]:
            weight[a][b] = weight[b][a] = c
    ans = []
    for _ in range(int(input())):
        c, s, e = map(int, input().split())
        ans.append(dijkstra(s, e, c))
    stdout.write('\n'.join(ans) + '\n')

main()