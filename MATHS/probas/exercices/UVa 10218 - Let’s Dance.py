import math

while True:
    M, W, C = map(int,input().split())
    if M == W == 0: break
    p = sum(
        pow(W / (W + M), C - 2 * i) * pow(M / (W + M), 2 * i) * math.comb(C, 2 * i)
        for i in range(C+2>>1)
    )
    print("{:.07f}".format(p))