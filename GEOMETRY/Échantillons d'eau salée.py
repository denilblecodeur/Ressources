def dist(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**.5

def get_proj(ax, ay, bx, by, mx, my):
    if ax == bx:
        return ax, my
    alpha = (by - ay) / (bx - ax)
    beta = by - bx * alpha
    xu, yu = bx - ax, by - ay
    hx = (mx * xu + my * yu - beta * yu) / (xu + alpha * yu)
    hy = alpha * hx + beta
    return hx, hy

for _ in range(int(input())):
    ax, ay = map(float,input().split())
    bx, by = map(float,input().split())
    cx, cy = map(float,input().split())
    mx, my = map(float,input().split())

    alt = round(2 * dist((mx, my), (bx, by)), 6)
    
    if (ax - bx) * (cx - bx) + (ay - by) * (cy - by) < 0: # scalaire neg -> angle obtu
        print(alt)
        continue

    m1 = get_proj(bx, by, ax, ay, mx, my)
    m1 = [2 * m1[0] - mx, 2 * m1[1] - my]
    
    m2 = get_proj(bx, by, cx, cy, mx, my)
    m2 = [2 * m2[0] - mx, 2 * m2[1] - my]

    print(round(dist(m1, m2), 6))