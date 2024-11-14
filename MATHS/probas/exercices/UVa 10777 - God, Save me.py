import sys
input = sys.stdin.buffer.readline

for tc in range(int(input())):
    line = input()
    while line == b'\n': line = input()
    n = int(line)
    psuccess = pfail = sp = 0
    for _ in range(n):
        x, p = input().split()
        x, p = int(x), float(p)
        if x>0:
            psuccess += p * x
        else:
            pfail += p * (-x)
            sp += p
    if sp == 1:
        print("Case {}: God! Save me".format(tc+1))
    else:
        E = (psuccess + pfail) / (1 - sp)
        print("Case {}: {:.02f}".format(tc+1, E))