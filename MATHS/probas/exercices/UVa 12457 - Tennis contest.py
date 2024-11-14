import sys, math
input = sys.stdin.buffer.readline

for _ in range(int(input())):
    n = int(input())
    p = float(input())
    ans = 0
    for i in range(n):
        ans += (1-p)**i * p**n * math.comb(n-1+i, i)
    print("{:.2f}".format(ans))