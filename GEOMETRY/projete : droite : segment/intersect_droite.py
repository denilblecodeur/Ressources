def intersect_droite():

    ax, ay, bx, by = map(float,input().split())
    cx, cy, dx, dy = map(float,input().split())

    xAB, yAB = bx - ax, by - ay
    xCD, yCD = dx - cx, dy - cy
    xAC, yAC = cx - ax, cy - ay

    t = ( xAC * yCD - yAC * xCD ) / ( xAB * yCD - yAB * xCD )
    
    X = ax + t * xAB
    Y = ay + t * yAB

    return X, Y

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

print(line_intersection((A, B), (C, D)))

dx = x - a.x
dy = y - a.y

dx = x - b.x
dy = y - b.y

ray_intersect = (dx > 0) == (vb.x > 0) and (dy > 0) == (vb.y > 0) and (dx > 0) == (va.x > 0) and (dy > 0) == (va.y > 0)