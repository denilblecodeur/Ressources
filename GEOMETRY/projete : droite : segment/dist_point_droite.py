def dist_point_droite(xa, ya, xb, yb, xm, ym):
    xu, yu = xb - xa, yb - ya
    a = yu
    b = -xu
    c = xu * ya - yu * xa
    return abs(a * xm + b * ym + c) / ( (a**2 + b**2) )**.5

# distance entre projeté orthogonal d'un point M
# sur droite AB et point A de la droite
def dist_point_droite(xa, ya, xb, yb, xm, ym):
    xAB = xb - xa
    yAB = yb - ya
    normeAB = ( (xAB)**2 + (yAB)**2 )**.5
    xAP = xm - xa
    yAP = ym - ya
    return (xAB * xAP + yAB * yAP) / normeAB