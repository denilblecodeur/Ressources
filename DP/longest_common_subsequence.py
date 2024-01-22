# Longest Common Subsequence of two strings
a = input()
b = input()
dp = [[0] * (len(a) + 1) for _ in range(len(b) + 1)]
for i in range(1, len(b) + 1):
    for j in range(1, len(a) + 1):
        if b[i - 1] == a[j - 1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

print(dp[len(b)][len(a)])

# construct lcs

i, j = len(b), len(a)
rec = []
while i > 0 and j > 0:
    if b[i - 1] == a[j - 1]:
        rec.append(b[i - 1])
        i -= 1
        j -= 1
    elif dp[i - 1][j] > dp[i][j - 1]:
        i -= 1
    else:
        j -= 1
print(''.join(rec[::-1]))

# construct whole interleaving
i, j = len(b), len(a)
rec = []
while i > 0 and j > 0:
    if b[i - 1] == a[j - 1]:
        rec.append(b[i - 1])
        i -= 1
        j -= 1
    elif dp[i - 1][j] > dp[i][j - 1]:
        rec.append(b[i - 1])
        i -= 1
    else:
        rec.append(a[j - 1])
        j -= 1
while i > 0:
    rec.append(b[i - 1])
    i -= 1
while j > 0:
    rec.append(a[j - 1])
    j -= 1

print(''.join(rec[::-1]))