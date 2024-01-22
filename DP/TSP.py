dp = [[-1] * (1<<n) for _ in range(n)]

def F(i, mask):
    mask ^= (1<<i)
    if mask == 0:
        return dist[i][0]
    if dp[i][mask] != -1:
        return dp[i][mask]
    dp[i][mask] = 1<<20
    for bit in range(n):
        if mask & (1<<bit):
            dp[i][mask] = min(dp[i][mask], F(bit, mask) + dist[i][bit])
    return dp[i][mask]

F(0, (1 << n) - 1)

# retrieve path

def tsp_dp():
    dp = [[-1] * (1<<n) for _ in range(n)]
    _next = [[-1] * (1<<n) for _ in range(n)]
    def F(i, mask):
        mask ^= (1<<i)
        if mask == 0:
            return dist[i][0]
        if dp[i][mask] != -1:
            return dp[i][mask]
        dp[i][mask] = 1<<59
        for bit in range(n):
            if mask & (1<<bit):
                new = F(bit, mask) + dist[i][bit]
                if new < dp[i][mask]:
                    dp[i][mask] = new
                    _next[i][mask] = bit
        return dp[i][mask]
    F(0, (1 << n) - 1)
    path = []
    node, mask = 0, (1 << n) - 1
    while node != -1:
        mask ^= (1 << node)
        path.append(node)
        node = _next[node][mask]
    path.append(0)
    return path