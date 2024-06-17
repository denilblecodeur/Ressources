eps = 1e-7

def dot(p, q):
    return p[0]*q[0]+p[1]*q[1]
def _cross(p, q):
    return p[0]*q[1]-p[1]*q[0]
def cross(p, a, b):
    return _cross((a[0]-p[0],a[1]-p[1]), (b[0]-p[0],b[1]-p[1]))

def onSegment(s, e, p):
	return -eps<cross(p, s, e)<eps and dot((s[0]-p[0],s[1]-p[1]),(e[0]-p[0],e[1]-p[1]))<eps

def inPolygon(points, a, strict=True):
    cnt, n = 0, len(points)
    for i in range(n):
        p, q = points[i], points[(i+1)%n]
        if onSegment(p, q, a): return not strict
        cnt ^= ((a[1]<p[1]) - (a[1]<q[1])) * cross(a, p, q) > eps
    return cnt

n = int(input())
points = [tuple(map(int,input().split())) for _ in range(n)]
for _ in range(int(input())):
    x, y = map(int,input().split())
    print(int(inPolygon(points, (x, y))))