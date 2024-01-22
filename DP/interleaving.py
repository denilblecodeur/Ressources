# Test if string C is an interleaving of strings a and b

a = input()
b = input()
c = input()

if len(a) + len(b) != len(c):
    print('NO') & exit()

dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]

for i in range(len(a) + 1):
    for j in range(len(b) + 1):

        if i == 0 and j == 0:
            dp[i][j] = 1
        
        elif i == 0 and b[j - 1] == c[j - 1]:
            dp[i][j] = dp[i][j - 1]
        
        elif j == 0 and a[i - 1] == c[i - 1]:
            dp[i][j] = dp[i - 1][j]
        
        else:
            if a[i - 1] == c[i + j - 1]:
                dp[i][j] = dp[i - 1][j]
            if b[j - 1] == c[i + j - 1]:
                dp[i][j] |= dp[i][j - 1]

print('YES' if dp[len(a)][len(b)] else 'NO')