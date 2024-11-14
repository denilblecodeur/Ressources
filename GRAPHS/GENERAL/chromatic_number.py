"""
Minimum Clique Cover <=> Graph Coloring of Complement Graph
Kattis : Square Fields (Hard)

Constraints : N <= 20
No multiples or self edge
"""

def chromatic_number(n: int, edges: list[tuple[int, int]]) -> int:
    def popcount(x):
        x = ((x >> 1)  & 0x55555555) + (x & 0x55555555)
        x = ((x >> 2)  & 0x33333333) + (x & 0x33333333)
        x = ((x >> 4)  & 0x0f0f0f0f) + (x & 0x0f0f0f0f)
        x = ((x >> 8)  & 0x00ff00ff) + (x & 0x00ff00ff)
        x = ((x >> 16) & 0x0000ffff) + (x & 0x0000ffff)
        return x
    def ctz(x):
        return popcount(~x & (x - 1))
    edge = [0] * n
    for uv in edges:
        u, v = uv
        edge[u] |= 1 << v
        edge[v] |= 1 << u
    dp = [0] * (1 << n)
    dp[0] = 1
    cur = [0] * (1 << n)
    for bit in range(1, 1 << n):
        v = ctz(bit)
        dp[bit] = dp[bit ^ (1 << v)] + dp[(bit ^ (1 << v)) & (~edge[v])]
    for bit in range(1 << n):
        if (n - popcount(bit)) & 1:
            cur[bit] = -1
        else:
            cur[bit] = 1
    for k in range(1, n):
        tmp = 0
        for bit in range(1 << n):
            cur[bit] *= dp[bit]
            tmp += cur[bit]
        if tmp != 0:
            res = k
            break
    else:
        res = n
    return res