def multiply(A, B):
    C = [[0] * len(B[0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

@bootstrap
def power(M, p):
    if p==0:
        yield M
    if p&1:
        res = (yield power(M, p-1))
        yield multiply(M, res)
    res = (yield power(M, p>>1))
    yield multiply(res, res)

def binet(n):
    # fonctionne jusqu'à 72, en c++ 75 avec double
    phi = (1 + (5**.5)) / 2
    return (pow(phi, n) - pow(-phi, -n)) / 5**.5

mod = 10 ** 9 + 7
 
def multiply(A, B):
    C = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            for k in range(2):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C
 
def power(M, p):
    if p == 0:
        return [[1, 0], [0, 1]]
    if p & 1:
        res = power(M, p - 1)
        return multiply(M, res)
    res = power(M, p // 2)
    return multiply(res, res)
 
def fib(n):
    if abs(n) < 2:
        return abs(n)
    M = power([[1, 1], [1, 0]], abs(n) - 2)
    res = (M[0][0] + M[0][1]) % mod
    if n < 0 and n & 1 == 0:
        return -res
    return res