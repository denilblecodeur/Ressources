from math import hypot
from random import shuffle

def cercle_minimum(points):
    shuffled=[(float(x),float(y)) for (x,y) in points]
    shuffle(shuffled)
    c=None
    for (i,p) in enumerate(shuffled):
        if c is None or not is_in_circle(c,p):
            pts,c=shuffled[:i+1],(p[0],p[1],0.0)
            for (i,q) in enumerate(pts):
                if not is_in_circle(c,q):
                    if c[2] == 0.0:
                        c=make_diameter(p,q)
                    else:
                        c=_mk_circ_2_pts(pts[:i+1],p,q)
    return c # x, y, r
def _mk_circ_2_pts(points,p,q):
    circ,l,r=make_diameter(p,q),None,None
    px,py=p; qx,qy=q
    for pt in points:
        if is_in_circle(circ,pt):
            continue
        cross=xp(px,py,qx,qy,pt[0],pt[1])
        c=make_circumcircle(p,q,pt)
        xp1,xp2,xp3=[xp(px,py,qx,qy,e[0],e[1])if e is not None else None for e in [c,l,r]]
        if c is None:
            continue
        elif cross>0.0 and (l is None or xp1>xp2):
            l=c
        elif cross<0.0 and (r is None or xp1<xp3):
            r=c
    if l is None and r is None:
        return circ
    elif l is None:
        return r
    elif r is None:
        return l
    else:
        return l if (l[2] <= r[2]) else r

def make_diameter(a,b):
    cx,cy=(a[0]+b[0])/2,(a[1]+b[1])/2
    r0=hypot(cx-a[0],cy-a[1])
    r1=hypot(cx-b[0],cy-b[1])
    return (cx,cy,max(r0,r1))

def make_circumcircle(a,b,c):
    m=lambda abc,i,f:f([e[i] for e in abc])
    ox=(m((a,b,c),0,min)+m((a,b,c),0,max))/2
    oy=(m((a,b,c),1,min)+m((a,b,c),1,max))/2
    ax=a[0]-ox; ay=a[1]-oy; bx=b[0]-ox
    by=b[1]-oy; cx=c[0]-ox; cy=c[1]-oy
    d=(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))*2.0
    if d == 0.0: return None
    x=ox+((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
    y=oy+((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
    ra,rb=hypot(x-a[0],y-a[1]),hypot(x-b[0],y-b[1])
    rc=hypot(x-c[0],y-c[1])
    return (x,y,max(ra,rb,rc))

EPSILON=1+1e-14

def is_in_circle(c,p):
    return c is not None and hypot(p[0]-c[0],p[1]-c[1]) <= c[2]*EPSILON
def xp(x0,y0,x1,y1,x2,y2):
    return (x1-x0)*(y2-y0)-(y1-y0)*(x2-x0)