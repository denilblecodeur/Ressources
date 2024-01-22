def projete_ortho(ax, ay, bx, by, mx, my):
    if ax == bx:
        return ax, my
    alpha = (by - ay) / (bx - ax)
    beta = by - bx * alpha
    xu = bx - ax
    yu = by - ay
    hx = (mx * xu + my * yu - beta * yu) / (xu + alpha * yu)
    hy = alpha * hx + beta
    return hx, hy

def projete_ortho(ax, ay, bx, by, mx, my):
    if ax == bx:
        return ax, my

    xu, yu = xb - xa, yb - ya
    a = yu
    b = -xu
    c = xu * ya - yu * xa

    t = - (a * mx + b * my + c) / (a**2 + b**2)

    xh = a * t + xp
    yh = b * t + yp

    return xh, yh