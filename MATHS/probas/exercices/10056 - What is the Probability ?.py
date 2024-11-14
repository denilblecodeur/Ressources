for _ in range(int(input())):
    n, p, i = input().split()
    n, p, i = int(n), float(p), int(i)
    # 1 + (1-p)^n + (1-p)^2n + (1-p)^3n + ... = 1 / (1 - (1-p)^n)
    if p == 0:
        ans = 0
    else:
        ans = pow(1-p, i-1) * p / (1 - pow(1-p, n))
    print("{:.04f}".format(ans))