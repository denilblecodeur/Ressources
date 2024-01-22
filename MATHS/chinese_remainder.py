from math import prod

def bezout(a, b):
    px, py = 1, 0
    x, y = 0, 1
    while b != 0:
        a, (q, b) = b, divmod(a, b)
        px, x = x, px - q * x
        py, y = y, py - q * y
    return a, px, py

def invmod(a, n):
    gcd, inv, _ = bezout(a, n)
    if gcd != 1:
        return None
    return inv % n

# a is list of values
# n is list of modulos
def crt(a, n):
    x = 0
    p = prod(n)
    for ai, ni in zip(a, n):
        xi = p // ni
        try: inv = pow(xi, -1, ni)
        except ValueError: return None
        x += ai * xi * inv
    return x % p

# For non-coprime moduli
# https://cp-algorithms.com/algebra/chinese-remainder-theorem.html#solution-for-not-coprime-moduli
def crtNonCoprime(a, n):
    prime = {}
    for ai, ni in zip(a, n):
        for k, v in getPrimeFactors(ni).items():
            m = pow(k, v)
            aj, nj = prime.get(k, (ai % m, m))
            if aj != (ai % m) % nj:
                return None # TO CHECK
            if nj > m:
                continue
            prime[k] = (ai % m, m)
    new_a, new_n = [], []
    for k, (ai, ni) in prime.items():
        new_a.append(ai)
        new_n.append(ni)
    return crt(new_a, new_n)