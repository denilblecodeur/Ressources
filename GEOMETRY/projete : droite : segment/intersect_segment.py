def intersect(a,b,c,d):
    def ccw(a,b,c):
        cp = (a[0] - c[0]) * (b[1] - c[1]) - (a[1] - c[1]) * (b[0] - c[0])
        return 1 if cp > 0 else -1 if cp < 0 else 0
    def onSegment(a,b,c):
        in_x = min(a[0],b[0]) <= c[0] <= max(a[0],b[0])
        in_y = min(a[1],b[1]) <= c[1] <= max(a[1],b[1])
        return in_x and in_y
    if not (ccw(a,b,c) or ccw(a,b,d) or ccw(b,c,d) or ccw(a,c,d)):
        return onSegment(a,b,c) or onSegment(a,b,d) or onSegment(c,d,b) or onSegment(c,d,a)
    return ccw(a,b,c) != ccw(a,b,d) and ccw(b,c,d) != ccw(a,c,d)