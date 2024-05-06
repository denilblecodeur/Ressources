def floyd(x0, f):
    t = f(x0)
    h = f(f(x0))
    while t != h:
        t = f(t)
        h = f(f(h))
    start = 0
    t = x0
    while t != h:
        t = f(t)
        h = f(h)
        start += 1
    period = 1
    h = f(t)
    while t != h:
        h = f(h)
        period += 1
    return start, period

for cycle_len in range(2, 100):
    for start in range(len(mex)-2*cycle_len):
        if mex[start:start+cycle_len] == mex[start+cycle_len:start+2*cycle_len]:
            print(start, cycle_len)
            exit()