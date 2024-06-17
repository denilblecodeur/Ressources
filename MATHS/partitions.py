def generateur_partitions(n):
    def partition_suivante(a, k, N): 
        b = a[:k] + [a[k]-1]
        q, r = divmod((N+1), b[k])
        b = b + q*[b[k]] 
        if r!=0: b.append(r) 
        while b[k]!=1: 
            k+=1 
            if k==len(b): break 
        return (b, k-1, len(b) - k)
    p = [n] 
    yield p 
    k, N = (-1, 1) if n==1 else (0, 0) 
    while k >= 0: 
        p, k, N = partition_suivante(p, k, N) 
        yield p

partitions = [[] for _ in range(11)]
for k in range(1, 11):
    partitions[k] = generateur_partitions(k)