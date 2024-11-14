import sys

for line in sys.stdin.buffer:
    ncows, ncars, nshow = map(int,line.split())
    # chose cow, ncars / (ncows-1-nshow+ncars)
    # chose car, (ncars-1) / (ncows-nshow+ncars-1)
    win = ncows * (ncars / (ncows-1-nshow+ncars)) + ncars * ((ncars-1) / (ncows-nshow+ncars-1))
    print("{:.05f}".format(win / (ncows + ncars)))