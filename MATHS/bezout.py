def bezout(a, b):
    # Calcule une solution à l’équation ax + by = pgcd(a, b)
    px, py = 1, 0
    x, y = 0, 1
    while b != 0:
        a, (q, b) = b, divmod(a, b)
        px, x = x, px - q * x
        py, y = y, py - q * y
    return a, px, py # pgcd, x, y

def solve(a, b, n):
    g, x, y = bezout(a, b)
    if n % g:
        return -1
    # to get to ax + by = n
    x *= n // g
    y *= n // g
    # two equations of Linear Diophantine x = x0 + (b/d)n, y = y0 - (a/d)n, where n is an integer
    # derivation of n based on the fact that x and y have to be positive
    # x0 + (b/d)n >= 0, solve for n: we get n >= -x0*d/b
    # y0 - (a/d)n >= 0, solve for n: we get n <= y0*d/a
    # putting together -x0*d/b <= n <= y0*d/a
    lo = -((x * g) // b)
    hi = (y * g) // a
    if lo > hi:
        return -1
    return x + (b * lo) // g, y - (a * lo) // g

a, b, c = 25, 18, 839 # 25x + 18y = 839
print(solve(a, b, c))

"""
def solve(c1, a, c2, b):
    g, x, y = bezout(a, b)
    if n % g:
        return -1
    # to get to ax + by = n
    x *= n // g
    y *= n // g
    # two equations of Linear Diophantine x = x0 + (b/d)n, y = y0 - (a/d)n, where n is an integer
    # derivation of n based on the fact that x and y have to be positive
    # x0 + (b/d)n >= 0, solve for n: we get n >= -x0*d/b
    # y0 - (a/d)n >= 0, solve for n: we get n <= y0*d/a
    # putting together -x0*d/b <= n <= y0*d/a
    a //= g; b //= g  # divide first to prevent overflow
    lo = -(x // b)
    hi = y // a
    if lo > hi:
        return -1
    res1 = c1 * (x + b * lo) + c2 * (y - a * lo)
    res2 = c1 * (x + b * hi) + c2 * (y - a * hi)
    if res1 < res2:
        return x + b * lo, y - a * lo
    return x + b * hi, y - a * hi

while True:
    n = int(input())
    if n == 0: break
    c1, a = map(int,input().split())
    c2, b = map(int,input().split())
    ans = solve(c1, a, c2, b)
    if ans == -1:
        print('failed')
    else:
        print(*ans)
"""