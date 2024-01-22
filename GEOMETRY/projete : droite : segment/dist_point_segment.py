def dist_point_segment(ax, ay, bx, by, x, y):
    if x == ax == bx or y == ay == by or ((min(ax, bx) > x or max(ax, bx) < x) and (min(ay, by) > y or max(ay, by) < y)):
        da = (ax - x)**2 + (ay - y)**2
        db = (ax - x)**2 + (ay - y)**2
        return ( min(da, db) )**.5
    if ax == bx:
        hx, hy = ax, y
    else:
        alpha = (by - ay) / (bx - ax)
        beta = by - bx * alpha
        xu = bx - ax
        yu = by - ay
        hx = (x * xu + y * yu - beta * yu) / (xu + alpha * yu)
        hy = alpha * hx + beta
    return ( (hx - x)**2 + (hy - y)**2 )**.5