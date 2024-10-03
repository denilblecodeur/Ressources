# A - B <= w means edge B -> A with weight w
# SIM A B w -> A - B <= w and B - A <= w
# BEF A B w -> A - B <= -w
import sys
input = sys.stdin.readline
INF = 1<<59

def main():
    n, k = map(int,input().split())
    vtx_code = {}
    i = 1
    edges = []
    for _ in range(n):
        t, a, b, w = input().split()
        if a not in vtx_code:
            vtx_code[a] = i
            i += 1
        if b not in vtx_code:
            vtx_code[b] = i
            i += 1
        if t == 'BEF':
            edges.append((vtx_code[b], vtx_code[a], -int(w)))
        else:
            edges.append((vtx_code[b], vtx_code[a], int(w)))
            edges.append((vtx_code[a], vtx_code[b], int(w)))
    N = i + 1
    for vtx in range(1, N):
        edges.append((0, vtx, 0))

    D = [INF] * N
    D[0] = 0
    for _ in range(N + 1):
        changed = False
        for node, neigh, weight in edges:
            if D[node] + weight < D[neigh]:
                D[neigh] = D[node] + weight
                changed = True
    if changed:
        print('NO')
        return
    
    print('NO' if -min(D) > k else 'YES')

main()