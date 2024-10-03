"""
O(n^2)
"""
n = int(input())
X = set()
events = []
for _ in range(n):
    x1, y1, x2, y2 = [float(x) for x in input().split()]
    assert x1 <= x2 and y1 <= y2
    X.add(x1)
    X.add(x2)
    events.append((y1, 1, x1, x2))
    events.append((y2, -1, x1, x2))
i_to_x = list(sorted(X))
x_to_i = {xi: i for i, xi in enumerate(i_to_x)}
nb_current_rectangles = [0] * (len(i_to_x) - 1)
area = 0
length_union_intervals = 0
previous_y = 0
for y, offset, x1, x2 in sorted(events):
    area += (y - previous_y) * length_union_intervals
    i1 = x_to_i[x1]
    i2 = x_to_i[x2]
    for j in range(i1, i2):
        length_interval = i_to_x[j + 1] - i_to_x[j]
        if nb_current_rectangles[j] == 0:
            length_union_intervals += length_interval
        nb_current_rectangles[j] += offset
        if nb_current_rectangles[j] == 0:
            length_union_intervals -= length_interval
    previous_y = y
print(area)

"""
O(nlogn)
"""

n = int(input())
X, evt = [], []
for _ in range(n):
    x1, y1, x2, y2 = [float(x) for x in input().split()]
    X.append(x1)
    X.append(x2)
    evt.append((y1, 1, x1, x2))
    evt.append((y2, -1, x1, x2))
evt.sort()
X.sort()
sx = [X[0]]
for x in X:
    if sx[-1] < x: sx.append(x)
X = sx
L = [X[i+1] - X[i] for i in range(len(X)-1)]
x2i = {x:i for i, x in enumerate(X)}

N = 1 << len(L).bit_length()
c = [0] * (2 * N)  # covered
s = [0] * (2 * N)  # score
w = [0] * (2 * N)  # width
for i in range(len(L)):
    w[N + i] = L[i]
for k in range(N - 1, 0, -1):
    w[k] = w[k<<1] + w[k<<1|1]

def update(p, st, sp, l, r, d):
    if st + sp <= l or r <= st:
        return
    if l <= st and st + sp <= r:
        c[p] += d
    else:
        update(p<<1, st, sp>>1, l, r, d)
        update(p<<1|1, st+(sp>>1), sp>>1, l, r, d)
    if c[p] == 0:
        if p >= N:
            s[p] = 0
        else:
            s[p] = s[p<<1] + s[p<<1|1]
    else:
        s[p] = w[p]

def cover():
    return s[1]

last_y = 0
area = 0
for y, e, x1, x2 in evt:
    area += (y - last_y) * cover()
    last_y = y
    update(1, 0, N, x2i[x1], x2i[x2], e)

print(f"{round(area, 2):.2f}")