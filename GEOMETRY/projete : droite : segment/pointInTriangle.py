def pointInTriangle(p, a, b, c):
    def valid(a, b, c):
        d1, d2, d3 = dist(a, b), dist(b, c), dist(a, c)
        return sum((d1, d2, d3)) > 2 * max(d1, d2, d3)
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    d1 = sign(p, a, b)
    d2 = sign(p, b, c)
    d3 = sign(p, c, a)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)