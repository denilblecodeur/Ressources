import sys, math
input = sys.stdin.buffer.readline

while True:
    n, m = map(int,input().split())
    if n == m == 0: break
    b = []
    for _ in range(n):
        *l, a = map(int,input().split())
        b.append(a)
    tot = sum(b)
    for bi in b:
        g = math.gcd(bi, tot)
        print("{} / {}".format(bi//g, tot//g))