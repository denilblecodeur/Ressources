class BitTrie:
    def __init__(self, max_bit_len=32):
        self.inf = 1 << 63
        self.cc = [0]
        self.adj = [[-1], [-1]]
        self.mb = max_bit_len

    def add(self, a):
        u = 0
        self.cc[u] += 1
        for i in range(self.mb-1, -1, -1):
            d = a >> i & 1
            if self.adj[d][u] == -1:
                self.adj[d][u] = len(self.cc)
                self.adj[0].append(-1)
                self.adj[1].append(-1)
                self.cc.append(0)
            u = self.adj[d][u]
            self.cc[u] += 1

    def remove(self, a):
        if self.cc[0] == 0:
            return False
        uu = [0]
        u = 0
        for i in range(self.mb-1, -1, -1):
            d = a >> i & 1
            u = self.adj[d][u]
            if u == -1 or self.cc[u] == 0:
                return False
            uu.append(u)
        for u in uu:
            self.cc[u] -= 1
        return True

    def cnt(self, a):
        u = 0
        for i in range(self.mb-1, -1, -1):
            d = a >> i & 1
            u = self.adj[d][u]
            if u == -1 or self.cc[u] == 0:
                return 0
        return self.cc[u]

    def min_xor(self, a):
        if self.cc[0] == 0:
            return self.inf
        u, res = 0, 0
        for i in range(self.mb-1, -1, -1):
            d = a >> i & 1
            v = self.adj[d][u]
            if v == -1 or self.cc[v] == 0:
                res |= 1 << i
                u = self.adj[d ^ 1][u]
            else:
                u = v
        return res

    def max_xor(self, a):
        if self.cc[0] == 0:
            return -self.inf
        u, res = 0, 0
        for i in range(self.mb-1, -1, -1):
            d = a >> i & 1
            v = self.adj[d ^ 1][u]
            if v == -1 or self.cc[v] == 0:
                u = self.adj[d][u]
            else:
                u = v
                res |= 1 << i
        return res

# ALT

B = 29
N = 150000 * (B + 1)

class BitTrie:
    def __init__(self):
        self.idx = 0
        self.trie = [[0] * N for _ in range(2)]
        self.dp = [[0] * N for _ in range(2)]
 
    def new_node(self):
        self.idx += 1
        self.trie[0][self.idx] = self.trie[1][self.idx] = 0
        self.dp[0][self.idx] = self.dp[1][self.idx] = 0
        return self.idx

n = int(input())
bt = BitTrie()
bt.new_node()
for i, x in enumerate(map(int,input().split())):
    xi = x ^ i
    p = 1
    for j in range(B, -1, -1): # query
        v = xi >> j & 1
        t = bt.trie[v ^ 1][p]
        dp[i] = max(dp[i], bt.dp[i >> j & 1][t])
        p = bt.trie[v][p]
        if p == 0:
            break
    p = 1
    for j in range(B, -1, -1): # add
        v = xi >> j & 1
        t = bt.trie[v][p]
        if t == 0:
            bt.trie[v][p] = t = bt.new_node()
        p = t
        t = x >> j & 1
        bt.dp[t][p] = max(bt.dp[t][p], dp[i])