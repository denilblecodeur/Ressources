from random import randrange
from math import gcd


def is_prime(n):
    if n == 2:
        return 1
    if n == 1 or n%2 == 0:
        return 0

    m = n - 1
    lsb = m & -m
    s = lsb.bit_length()-1
    d = m // lsb
    if n < 4759123141:
        test_numbers = [2, 7, 61]
    elif n < 341550071728321:
        test_numbers = [2, 3, 5, 7, 11, 13, 17]
    elif n < 3825123056546413051:
        test_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    else:
        test_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

    for a in test_numbers:
        if a == n:
            continue
        x = pow(a,d,n)
        r = 0
        if x == 1:
            continue
        while x != m:
            x = pow(x,2,n)
            r += 1
            if x == 1 or r == s:
                return 0
    return 1


def find_prime_factor(n):
    m = max(1,int(n**0.125))

    while True:
        c = randrange(n)
        y = k = 0
        g = q = r = 1
        while g == 1:
            x = y
            mr = 3*r//4
            while k < mr:
                y = (pow(y,2,n)+c)%n
                k += 1
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r-k)):
                    y = (pow(y,2,n)+c)%n
                    q = q*abs(x-y)%n
                g = gcd(q,n)
                k += m
            k = r
            r <<= 1
        if g == n:
            g = 1
            y = ys
            while g == 1:
                y = (pow(y,2,n)+c)%n
                g = gcd(abs(x-y),n)
        if g == n:
            continue
        if is_prime(g):
            return g
        elif is_prime(n//g):
            return n//g
        else:
            return find_prime_factor(g)


def factorize(n):
    res = {}
    for p in range(2,1000):
        if p*p > n:
            break
        if n%p:
            continue
        s = 0
        while n%p == 0:
            n //= p
            s += 1
        res[p] = s

    while not is_prime(n) and n > 1:
        p = find_prime_factor(n)
        s = 0
        while n%p == 0:
            n //= p
            s += 1
        res[p] = s
    if n > 1:
        res[n] = 1
    return res

a = int(input())
f = factorize(a)
ans = [i for i,j in sorted(f.items()) for _ in range(j)]
print(len(ans),*ans)