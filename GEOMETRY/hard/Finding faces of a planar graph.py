from math import atan2, fsum
from collections import defaultdict, namedtuple

Point = namedtuple("p", "x y")

def shoelace(poly):
    fw = sum(poly[i - 1].x * poly[i].y for i in range(len(poly)))
    poly = list(reversed(poly))
    bw = sum(poly[i - 1].x * poly[i].y for i in range(len(poly)))
    return abs(fw - bw) / 2.0

def sort_ccw(p, points):
    return sorted(points, key=lambda point: atan2(point.y - p.y, point.x - p.x))

def find_face(neighbors, u, v):
    face = []
    current = v
    previous = u
    face.append(previous)
    while True:
        face.append(current)
        current_neighbors = neighbors[current]
        index = current_neighbors.index(previous)
        next_index = (index + 1) % len(current_neighbors)
        next_vertex = current_neighbors[next_index]
        if next_vertex == u:
            break
        previous, current = current, next_vertex
    face.append(u)
    return face

def find_outer_edge(coord):
    leftmost = min(coord, key=lambda p: (p.x, p.y))
    N_leftmost = coord[leftmost]
    sorted_neighbors = sorted(
        N_leftmost, key=lambda p: atan2(p.y - leftmost.y, p.x - leftmost.x)
    )
    u = sorted_neighbors[0]
    return (leftmost, u)

n = int(input())
coord = defaultdict(list)
for l in range(n):
    x1, y1, x2, y2 = map(float, input().split())
    p1, p2 = Point(x1, y1), Point(x2, y2)
    coord[p1].append(p2)
    coord[p2].append(p1)

for p in coord:
    coord[p] = sort_ccw(p, coord[p])

seen = set()

p, q = find_outer_edge(coord)
outer = find_face(coord, p, q)
for i in range(len(outer) - 1):
    seen.add((outer[i], outer[i + 1 % len(outer)]))

areas = []
for p in coord:
    for q in coord[p]:
        if (p, q) in seen:
            continue
        seen.add((p, q))
        face = find_face(coord, p, q)
        areas.append(shoelace(face) ** 2)
        for i in range(len(face) - 1):
            seen.add((face[i], face[i + 1 % len(face)]))

print(fsum(areas))