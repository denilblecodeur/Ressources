from random import *
from math import acos, degrees, dist

def genererPoints(n):
    points = [(randint(0, 1000), randint(0, 1000), i%2) for i in range(n)]
    for i in range(n):
        a = points[i]
        for j in range(i):
            b = points[j]
            for k in range(j):
                c = points[k]
                if (a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0]) == 0:
                    print("Re-générer points")
                    return genererPoints(n)
    return points

def scalaire(u, v):
    return (u[1][0] - u[0][0]) * (v[1][0] - v[0][0]) + (u[1][1] - u[0][1]) * (v[1][1] - v[0][1])

def norme(u):
    return dist(u[0], u[1])

def alpha(u, v, w, points):
    if u == w:
        return -1
    x0, y0, _ = points[u]
    x1, y1, _ = points[v]
    x2, y2, _ = points[w]
    u = ((x0, y0), (x1, y1))
    v = ((x0, y0), (x2, y2))
    return degrees(acos(round(scalaire(u, v) / (norme(u) * norme(v)), 5)))

n = int(input())
points = genererPoints(n)

def getOrder(points):
    u, v = None, None
    for i, (x, y, t) in enumerate(points):
        if u is None or y < points[u][1]:
            v, u = u, i
        elif v is None or y < points[v][1]:
            v = i
    return sorted(range(len(points)), key=lambda i:alpha(u, v, i, points))

matching = []

def solve(points):
    if not points: return
    if len(points) == 2:
        matching.append((points[0], points[1]))
        return
    order = getOrder(points)
    c, f = 0, 0
    if points[order[0]][2]: f += 1
    else: c += 1
    cur = 0
    while c != f:
        cur += 1
        if points[order[cur]][2]: f += 1
        else: c += 1
    matching.append((points[order[0]], points[order[cur]]))
    left, right = [], []
    for i in range(1, cur):
        left.append(points[order[i]])
    solve(left)
    for i in range(cur + 1, len(points)):
        right.append(points[order[i]])
    solve(right)

solve(points)

import matplotlib.pyplot as plt
plt.plot([x for x, y, t in points if t], [y for x, y, t in points if t], marker='o', color='r', ls='')
plt.plot([x for x, y, t in points if not t], [y for x, y, t in points if not t], marker='o', ls='')
for a, b in matching:
    plt.plot((a[0], b[0]), (a[1], b[1]), 'grey')
plt.show()