def greatDistance(pLat, pLong, qLat, qLong, radius):
    # Convert to radians
    pLat, pLong = radians(pLat), radians(pLong)
    qLat, qLong = radians(qLat), radians(qLong)
    return radius *\
    acos(cos(pLat)*cos(pLong)*cos(qLat)*cos(qLong)\
    +\
    cos(pLat)*sin(pLong)*cos(qLat)*sin(qLong) + sin(pLat)*sin(qLat))