# KMP & Z-algorithm

# longest prefix suffix
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0  # length of the previous longest prefix suffix
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # Try to find a smaller prefix that is also a suffix
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

# Z[i] is length of the longest substr starting from str[i]
# which is also a prefix of str[0..n-1]
#
# i + Z[i] == n -> prefix suffix
Z = [0] * n
l = r = 0
for i in range(1, n):
    if i <= r:
        Z[i] = min(Z[i - l], r - i + 1)
    while i + Z[i] < n and s[Z[i]] == s[i + Z[i]]:
        Z[i] += 1
    if i + Z[i] - 1 > r:
        l = i
        r = i + Z[i] - 1

# i + Z[i] >= n => period of length i