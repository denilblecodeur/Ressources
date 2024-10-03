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


def partitions(partitions_n):
    partitions_a = [0 for _ in range(partitions_n + 1)]
    k_ = 1
    y_ = partitions_n - 1
    while k_ != 0:
        x_ = partitions_a[k_ - 1] + 1
        k_ -= 1
        while 2 * x_ <= y_:
            partitions_a[k_] = x_
            y_ -= x_
            k_ += 1
        l_ = k_ + 1
        while x_ <= y_:
            partitions_a[k_] = x_
            partitions_a[l_] = y_
            yield partitions_a[: k_ + 2]
            x_ += 1
            y_ -= 1
        partitions_a[k_] = x_ + y_
        y_ = x_ + y_ - 1
        yield partitions_a[: k_ + 1]