# Gaussian elimination ####################

def gauss(a, n, m):
    ans = [[0] * n for _ in range(n)]
    for i in range(n):
        mx = i
        for j in range(i + 1, n):
            if abs(a[j][i]) > abs(a[mx][i]):
                mx = j
        if abs(a[mx][i]) < 1e-8:
            continue
        if i != mx:
            temp = a[i]
            a[i] = a[mx]
            a[mx] = temp
        for j in range(n):
            if i == j:
                continue
            temp = a[j][i] / a[i][i]
            for k in range(i, m):
                a[j][k] -= a[i][k] * temp
    for i in range(n):
        for j in range(n):
            ans[i][j] = a[i][n + j] / a[i][i]
    return ans

B = [[0] * 2 * n for _ in range(n)]
for i in range(n):
    for j, c in enumerate(map(int,input().split())):
        B[i][j] = c
    B[i][n + i] = 1
P = gauss(B, n, 2 * n)