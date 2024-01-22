# BITSET DP
MAX = 1000001
dp = [0] * MAX
dp[0] = 1
for x in a:
    for j in range(MAX - 1, x - 1, -1):
        dp[j] |= dp[j - x]

# is equivalent to
"""
bitset<1000001> dp;
dp.set(0);
for(int j = 0; j < n; j++){
    dp |= dp << s[j];
}
"""

# Bitwise operations

b = 0          # The empty bitset :)
b |= 1 << i    # Set
b & 1 << i     # Test
b &= ~(1 << i) # Reset
b ^= 1 << i    # Flip i
b = ~b         # Flip all
def popcount(x):
    x = ((x >> 1)  & 0x55555555) + (x & 0x55555555)
    x = ((x >> 2)  & 0x33333333) + (x & 0x33333333)
    x = ((x >> 4)  & 0x0f0f0f0f) + (x & 0x0f0f0f0f)
    x = ((x >> 8)  & 0x00ff00ff) + (x & 0x00ff00ff)
    x = ((x >> 16) & 0x0000ffff) + (x & 0x0000ffff)
    return x
def bit_reverse(x):
    x = (x >> 16) | (x << 16)
    x = ((x >> 8) & 0x00FF00FF) | ((x << 8) & 0xFF00FF00)
    x = ((x >> 4) & 0x0F0F0F0F) | ((x << 4) & 0xF0F0F0F0)
    x = ((x >> 2) & 0x33333333) | ((x << 2) & 0xCCCCCCCC)
    x = ((x >> 1) & 0x55555555) | ((x << 1) & 0xAAAAAAAA)
    return x
def ctz(x): return popcount(~x & (x - 1))
def clz(x): return ctz(bit_reverse(x))

# get addition
a + b = (a|b) + (a&b)

# get xor
x = a&b
num = (a|b).bit_length()
!x = (1<<num) - 1 - x
a ^ b = !(a&b) & (a|b)
def flip(x, num): return (1<<num) - 1 - x

#BITSET CLASS

class Bitset:
    def _popcount(self, x):
        """ number of bits that are set to true """
        # Divide into groups of 2 bits and represent the number of set bits with 2 bits
        x = x - ((x >> 1) & 0x5555555555555555)
        # Put the value calculated by upper 2bit + lower 2bit into 4bit integer
        x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333)
        x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f  # Every 8bit
        x = x + (x >> 8)  # Every 16bit
        x = x + (x >> 16)  # Every 32bit
        x = x + (x >> 32)  # Every 64bit = sum of all
        return x & 0x0000007f
 
    def __init__(self, n):
        self.x = [0] * (n // 63 + 1)
        self.n = n
        pow2 = [1]
        for _ in range(62):
            pow2.append(2 * pow2[-1])
        self.sp = list(pow2)
        for i in range(1, 63):
            self.sp[i] ^= self.sp[i - 1]
 
    def __getitem__(self, item):
        i, j = item // 63, item % 63
        return (self.x[i] >> j) & 1
 
    def __setitem__(self, key, value):
        i, j = key // 63, key % 63
        self.x[i] |= 1 << j
        if value == 0:
            self.x[i] -= (1 << j)
 
    def popcount(self):
        c = 0
        for y in self.x: c += self._popcount(y)
        return c
 
    def __and__(self, other):
        res = bitset(self.n)
        for i in range(len(self.x)):
            res.x[i] = self.x[i] & other.x[i]
        return res
 
    def __or__(self, other):
        res = bitset(self.n)
        for i in range(len(self.x)):
            res.x[i] = self.x[i] | other.x[i]
        return res
 
    def __rshift__(self, other):
        res = bitset(self.n)
        res.x = self.x[:]
        k = other // 63
        if k:
            for i in range(len(self.x)):
                if i >= k:
                    res.x[i - k] = res.x[i]
                res.x[i] = 0
        d = other % 63
        if d:
            mask = 2 ** d - 1
            res.x[0] >>= d
            for i in range(1, len(self.x)):
                bf = res.x[i] & mask
                res.x[i] >>= d
                res.x[i - 1] |= bf << (63 - d)
        return res
 
    def __lshift__(self, other):
        res = bitset(self.n)
        res.x = self.x[:]
        k = other // 63
        m = len(self.x)
        if k:
            for i in range(m - 1, -1, -1):
                if i + k < m:
                    res.x[i + k] = res.x[i]
                res.x[i] = 0
        d = other % 63
        if d:
            mask = 2 ** (63 - d) - 1
            res.x[m - 1] &= mask
            res.x[m - 1] <<= d
            for i in range(m - 2, -1, -1):
                bf = res.x[i] >> (63 - d)
                res.x[i] &= mask
                res.x[i] <<= d
                res.x[i + 1] |= bf
        return res
 
    def __repr__(self):
        res = []
        for i in range(self.n): res.append(self[i])
        return ''.join(map(str,res))[::-1]
 
    def op(self, other):
        u, v = other // 63, other % 63
        m = len(self.x)
        if other:
            for j in range(m - 1, -1, -1):
                if not self.x[j]:
                    continue
                tmp = self.x[j]
                if u + j < m:
                    self.x[u + j] |= (tmp & self.sp[63 - v - 1]) << v
                    if u + j + 1 < m:
                        self.x[u + j + 1] |= tmp >> (63 - v)