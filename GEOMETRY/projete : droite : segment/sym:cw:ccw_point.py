def sym(p, o):
    px, py = p
    ox, oy = o
    return 2 * ox - px, 2 * oy - py

def rotate_cw(p, o):
    px, py = p
    ox, oy = o
    return ox - oy + py, ox + oy - px

def rotate_ccw(p, o):
    px, py = p
    ox, oy = o
    return ox + oy - py, oy - ox + px