# Tested on Kattis
# Suffix Array and LCP : Suffix Sorting, Stammering Aliens
# LCS : Life Forms, Longest Common Substring
# LRS : Dvaput
# Unique Substrings : Repeated Substrings

# Others applications :
# - Comparing two substrings of a string (cp alg)

def gen_suffix_array_and_lcp(words):
    def radix_sort(p_, c_):
        count = [0 for _ in range(len(p_))]
        for x in p_:
            count[c_[x]] += 1
        new_p = p_.copy()
        pos = [0 for _ in range(len(p_))]
        for i in range(1, len(p_)):
            pos[i] = pos[i-1] + count[i-1]
        for x in p_:
            new_p[pos[c_[x]]] = x
            pos[c_[x]] += 1
        return new_p
    s_ = []
    sep = 0
    sidx = []
    for idx, word in enumerate(words):
        for char in word:
            s_.append(len(words) + ord(char))
            sidx.append(idx)
        s_.append(sep)
        sidx.append(-1)
        sep += 1
    n = len(s_)
    a = [(s_[i], i) for i in range(n)]
    a.sort(key=lambda x: x[0])
    sufarr = [a[i][1] for i in range(n)]
    c = [0] * n
    c[sufarr[0]] = 0
    for i in range(1, n):
        if a[i][0] == a[i-1][0]:
            c[sufarr[i]] = c[sufarr[i-1]]
        else:
            c[sufarr[i]] = c[sufarr[i-1]] + 1
    k = 1
    while (1 << k) <= 2*n:
        sufarr = [(sufarr[i] - (1 << (k-1))) % n for i in range(n)]
        sufarr = radix_sort(sufarr, c)
        c_new = [0] * n
        prev = (c[sufarr[0]], c[(sufarr[0] + (1 << (k-1))) % n])
        for i in range(1, n):
            curr = (c[sufarr[i]], c[(sufarr[i] + (1 << (k-1))) % n])
            if prev == curr:
                c_new[sufarr[i]] = c_new[sufarr[i-1]]
            else:
                c_new[sufarr[i]] = c_new[sufarr[i-1]] + 1
            prev = curr
        c = c_new
        k += 1
        if c_new[sufarr[n-1]] == n - 1:
            break
    # sufarr is done generating
    lcp = [0] * (n-1)
    k = 0
    for i in range(n-1):
        pi = c[i]
        j = sufarr[pi - 1]
        while s_[i+k] == s_[j+k]:
            k += 1
        lcp[pi-1] = k
        k = max(k-1, 0)
    suf2s = [sidx[sufarr[i]] for i in range(len(words), n)]
    sufarr = sufarr[len(words):]
    lcp = lcp[len(words)-1:]
    return sufarr, lcp, suf2s, s_

def longest_common_substring(strings, k):
    # longest common substring such that k strings shares it
    n = len(strings)
    if n == 1: return len(strings[0]), [strings[0]]
    assert k > 1
    sufarr, lcp, suf2s, text = gen_suffix_array_and_lcp(strings)
    st = SparseTable(lcp)
    l = 0
    sn = [0] * n
    sn[suf2s[0]] += 1
    zeros = n-1
    lcs = 0
    start_idx = []
    for r in range(1, len(lcp)):
        if sn[suf2s[r]] == 0:
            zeros -= 1
        sn[suf2s[r]] += 1
        while (n - zeros) >= k:
            minimum = st.prod(l+1, r+1)
            if minimum > lcs:
                lcs = minimum
                start_idx = [sufarr[r]]
            elif minimum == lcs:
                start_idx.append(sufarr[r])
            sn[suf2s[l]] -= 1
            if sn[suf2s[l]] == 0:
                zeros += 1
            l += 1
    if lcs == 0: return 0, []
    substrings = sorted(''.join(chr(char - n) for char in text[st:st+lcs])
                        for st in start_idx)
    last, res = None, []
    for subs in substrings:
        if subs != last: res.append(subs)
        last = subs
    return lcs, res

def longest_repeated_substring(s):
    # overlap is OK : 'abrabra' -> 'abra'
    sufarr, lcp, _, _ = gen_suffix_array_and_lcp([s])
    lrs = max(lcp)
    if lrs == 0: return 0, []
    substrings = []
    for i in range(len(lcp)):
        if lcp[i] == lrs:
            substrings.append(s[sufarr[i]:sufarr[i]+lrs])
    substrings.sort()
    last, res = None, []
    for subs in substrings:
        if subs != last: res.append(subs)
        last = subs
    return lrs, res

def count_unique_substrings(s):
    _, lcp, _, _ = gen_suffix_array_and_lcp([s])
    # return len(set(substrings of s))
    return (len(s)*(len(s)+1)>>1) - sum(lcp)

def count_repeated_substrings(s):
    _, lcp, _, _ = gen_suffix_array_and_lcp([s])
    return sum(max(lcp[i] - lcp[i-1], 0) for i in range(1, len(lcp)))

def minRotation(s):
    # Duval O(n)
    a,N=0,len(s)
    s+=s
    for b in range(N):
        for k in range(N):
            if a+k==b or s[a+k]<s[b+k]:b+=max(0,k-1);break
            if s[a+k]>s[b+k]:a=b;break
    return a