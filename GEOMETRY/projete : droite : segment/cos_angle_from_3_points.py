def cos_angle_from_3_points(a, b, c): # a is corner
    ab = (a[0]-b[0])**2 + (a[1]-b[1])**2
    ac = (a[0]-c[0])**2 + (a[1]-c[1])**2
    bc = (c[0]-b[0])**2 + (c[1]-b[1])**2
    if ab * ac == 0:
        return float('inf')
    return abs((ab + ac - bc) / (2 * ab**.5 * ac**.5))