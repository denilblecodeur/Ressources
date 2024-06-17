# INDEXED SPACE
# Get number of pairs of points with dist < K
# Works when number of pairs < 10**6

SIZE = 1000
def dist(a, b): return (a[0] - b[0])**2 + (a[1] - b[1])**2

DIR = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1))
indexed_space = {}
for x, y in points:
    coord = (x // SIZE, y // SIZE)
    if indexed_space.get(coord, None) is None:
        indexed_space[coord] = []
    indexed_space[coord].append((x, y))

ans = 0
for coord, pts in indexed_space.items():
    x, y = coord
    for dx, dy in DIR:
        for p_neigh in indexed_space.get((x + dx, y + dy), []):
            for p in pts:
                if dist(p, p_neigh) <= K ** 2:
                    ans += 1
    for i in range(len(pts)):
        for j in range(i):
            if dist(pts[i], pts[j]) <= K ** 2:
                    ans += 2

print(ans // 2)