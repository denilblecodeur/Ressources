def minRotation(s):
    # Duval O(n)
    a,N=0,len(s)
    s+=s
    for b in range(N):
        for k in range(N):
            if a+k==b or s[a+k]<s[b+k]:b+=max(0,k-1);break
            if s[a+k]>s[b+k]:a=b;break
    return a