# https://www.hackerrank.com/topics/manachers-algorithm

def longest_palindromic_substring(s):
    # Preprocess the string to insert '#' between each character to handle even-length palindromes
    t = '#'.join('^{}$'.format(s))
    n = len(t)
    p = [0] * n
    center, right = 0, 0
 
    for i in range(1, n - 1):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
 
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
 
        if i + p[i] > right:
            center, right = i, i + p[i]
 
    max_len = max(p)
    center_index = p.index(max_len)
    start_index = (center_index - max_len) // 2
    return s[start_index:start_index + max_len]
 
a = input()
print(longest_palindromic_substring(a))