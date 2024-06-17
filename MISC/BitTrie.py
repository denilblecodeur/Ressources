class BinaryTrieXor:
    def __init__(self, nb_values, max_num=(1<<32)):
        max_num = max(max_num, 1)
        nb_values = max(nb_values, 1)
        binary_state = 2
        self.max_bit = max_num.bit_length() - 1
        self.cnt_bit = nb_values.bit_length()
        self.node_cnt = (self.max_bit + 1) * nb_values * binary_state
        self.son_and_cnt = [0] * (self.node_cnt + 1)
        self.ind = 1
        self.mask = (1 << self.cnt_bit) - 1
 
    def initial(self): # to retrieve init state
        for i in range(self.node_cnt + 1): self.son_and_cnt[i] = 0
        self.ind = 1

    def add(self, num: int, c=1) -> bool:
        cur = 0
        self.son_and_cnt[cur] += c
        for k in range(self.max_bit, -1, -1):
            bit = (num >> k) & 1
            if not self.son_and_cnt[(cur << 1) | bit] >> self.cnt_bit:
                self.son_and_cnt[(cur << 1) | bit] |= (self.ind << self.cnt_bit)
                self.ind += 1
            cur = self.son_and_cnt[(cur << 1) | bit] >> self.cnt_bit
            self.son_and_cnt[cur] += c
        return True
 
    def remove(self, num: int, c=1) -> bool:
        if self.son_and_cnt[0] & self.mask < c: return False
        cur = 0
        self.son_and_cnt[0] -= c
        for k in range(self.max_bit, -1, -1):
            bit = (num >> k) & 1
            cur = self.son_and_cnt[(cur << 1) | bit] >> self.cnt_bit
            if cur == 0 or self.son_and_cnt[cur] & self.mask < c: return False
            self.son_and_cnt[cur] -= c
        return True
 
    def count(self, num: int):
        cur = 0
        for k in range(self.max_bit, -1, -1):
            bit = (num >> k) & 1
            cur = self.son_and_cnt[(cur << 1) | bit] >> self.cnt_bit
            if cur == 0 or self.son_and_cnt[cur] & self.mask == 0: return 0
        return self.son_and_cnt[cur] & self.mask
 
    def get_maximum_xor(self, x: int) -> int:
        """get maximum result for constant x ^ element in array"""
        if self.son_and_cnt[0] & self.mask == 0: return float('-inf')
        res = cur = 0
        for k in range(self.max_bit, -1, -1):
            bit = (x >> k) & 1
            nxt = self.son_and_cnt[(cur << 1) | (bit ^ 1)] >> self.cnt_bit
            if nxt == 0 or self.son_and_cnt[nxt] & self.mask == 0:
                cur = self.son_and_cnt[(cur << 1) | bit] >> self.cnt_bit
            else:
                res |= 1 << k
                cur = nxt
        return res
 
    def get_minimum_xor(self, x: int) -> int:
        """get minimum result for constant x ^ element in array"""
        if self.son_and_cnt[0] & self.mask == 0: return float('inf')
        res = cur = 0
        for k in range(self.max_bit, -1, -1):
            bit = (x >> k) & 1
            nxt = self.son_and_cnt[(cur << 1) | bit] >> self.cnt_bit
            if nxt == 0 or self.son_and_cnt[nxt] & self.mask == 0:
                res |= 1 << k
                cur = self.son_and_cnt[(cur << 1) | (bit ^ 1)] >> self.cnt_bit
            else:
                cur = nxt
        return res
 
    def get_kth_maximum_xor(self, x: int, rk) -> int:
        """get kth maximum result for constant x ^ element in array"""
        assert rk >= 1
        if self.son_and_cnt[0] & self.mask < rk: return float('-inf')
        res = cur = 0
        for k in range(self.max_bit, -1, -1):
            bit = (x >> k) & 1
            nxt = self.son_and_cnt[(cur << 1) | (bit ^ 1)] >> self.cnt_bit
            if nxt == 0 or self.son_and_cnt[nxt] & self.mask < rk:
                if nxt: rk -= self.son_and_cnt[nxt] & self.mask
                cur = self.son_and_cnt[(cur << 1) | bit] >> self.cnt_bit
            else:
                res |= 1 << k
                cur = nxt
        return res
 
    def get_cnt_smaller_xor(self, x: int, y: int) -> int:
        """get cnt result for constant x ^ element <= y in array"""
        if self.son_and_cnt[0] & self.mask == 0: return 0
        res = cur = 0
        for k in range(self.max_bit, -1, -1):
            bit = (x >> k) & 1
            if not (y >> k) & 1:
                nxt = self.son_and_cnt[(cur << 1) | bit] >> self.cnt_bit
                if nxt == 0 or self.son_and_cnt[nxt] & self.mask == 0: return res
                cur = nxt
            else:
                nxt = self.son_and_cnt[(cur << 1) | bit] >> self.cnt_bit
                if nxt: res += self.son_and_cnt[nxt] & self.mask
                nxt = self.son_and_cnt[(cur << 1) | (bit ^ 1)] >> self.cnt_bit
                if nxt == 0 or self.son_and_cnt[nxt] & self.mask == 0: return res
                cur = nxt
        res += self.son_and_cnt[cur] & self.mask
        return res

class BitTrie:
    def __init__(self, max_bit_len=32):
        self.inf = 1 << 63
        self.cc = [0]
        self.adj = [[-1], [-1]]
        self.mb = max_bit_len

    def add(self, x):
        u = 0
        self.cc[u] += 1
        for i in range(self.mb-1, -1, -1):
            d = x >> i & 1
            if self.adj[d][u] == -1:
                self.adj[d][u] = len(self.cc)
                self.adj[0].append(-1)
                self.adj[1].append(-1)
                self.cc.append(0)
            u = self.adj[d][u]
            self.cc[u] += 1

    def remove(self, x):
        if self.cc[0] == 0:
            return False
        uu = [0]
        u = 0
        for i in range(self.mb-1, -1, -1):
            d = x >> i & 1
            u = self.adj[d][u]
            if u == -1 or self.cc[u] == 0:
                return False
            uu.append(u)
        for u in uu:
            self.cc[u] -= 1
        return True

    def cnt(self, x):
        u = 0
        for i in range(self.mb-1, -1, -1):
            d = x >> i & 1
            u = self.adj[d][u]
            if u == -1 or self.cc[u] == 0:
                return 0
        return self.cc[u]

    def min_xor(self, x):
        if self.cc[0] == 0:
            return self.inf
        u, res = 0, 0
        for i in range(self.mb-1, -1, -1):
            d = x >> i & 1
            v = self.adj[d][u]
            if v == -1 or self.cc[v] == 0:
                res |= 1 << i
                u = self.adj[d ^ 1][u]
            else:
                u = v
        return res

    def max_xor(self, x):
        if self.cc[0] == 0:
            return -self.inf
        u, res = 0, 0
        for i in range(self.mb-1, -1, -1):
            d = x >> i & 1
            v = self.adj[d ^ 1][u]
            if v == -1 or self.cc[v] == 0:
                u = self.adj[d][u]
            else:
                u = v
                res |= 1 << i
        return res

# ALTERNATIVE

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