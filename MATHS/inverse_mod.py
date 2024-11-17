"""
900 = 24*37+12 -> 900-24*37=12
37=3*12+1 -> 37-3*(900-24*37)=1
Therefore 73*37-3*900=1. So the inverse of 37 mod 900 is 73.
"""

x, y = 0, 1
def gcdExtended(a, b):
    global x, y
    if (a == 0):
        x, y = 0, 1
        return b
    gcd = gcdExtended(b % a, a)
    x1 = x
    y1 = y
    x, y = y1 - (b // a) * x1, x1
    return gcd

def modInverse(A, M):
    g = gcdExtended(A, M)
    if (g != 1):
        print("Inverse doesn't exist")
    else:
        # m is added to handle negative x
        res = (x % M + M) % M
        print("Modular multiplicative inverse is", res)