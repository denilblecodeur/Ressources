import bisect
import heapq
import math
import random
import statistics
import sys
from bisect import bisect_left as lower_bound
from bisect import bisect_right as upper_bound
from collections import Counter, defaultdict, deque
from copy import deepcopy
from datetime import datetime
from fractions import Fraction
from functools import lru_cache
from itertools import (
    permutations, combinations  # difference is that order matters for permutations but not for combinations
)

def gen_suffix_array(s_: str) -> list[int]:
    def radix_sort(p_: list[int], c_: list[int]) -> list[int]:
        count: list[int] = [0 for _ in range(len(p_))]
        for x in p_:
            count[c_[x]] += 1
        new_p: list[int] = p_.copy()
        pos: list[int] = [0 for _ in range(len(p_))]
        for i in range(1, len(p_)):
            pos[i] = pos[i-1] + count[i-1]
        for x in p_:
            new_p[pos[c_[x]]] = x
            pos[c_[x]] += 1

        return new_p
    s_ += "$"
    n: int = len(s_)
    a: list[tuple[str, int]] = [(s_[i], i) for i in range(n)]
    a.sort(key=lambda x: x[0])
    p: list[int] = [a[i][1] for i in range(n)]
    c: list[int] = [0] * n
    c[p[0]] = 0
    for i in range(1, n):
        if a[i][0] == a[i-1][0]:
            c[p[i]] = c[p[i-1]]
        else:
            c[p[i]] = c[p[i-1]] + 1
    k: int = 1
    while (1 << k) <= 2*n:
        p = [(p[i] - (1 << (k-1))) % n for i in range(n)]
        p = radix_sort(p, c)

        c_new: list[int] = [0] * n
        prev: tuple[int, int] = (c[p[0]], c[(p[0] + (1 << (k-1))) % n])
        for i in range(1, n):
            curr: tuple[int, int] = (c[p[i]], c[(p[i] + (1 << (k-1))) % n])
            if prev == curr:
                c_new[p[i]] = c_new[p[i-1]]
            else:
                c_new[p[i]] = c_new[p[i-1]] + 1
            prev = curr
        c = c_new
        k += 1
        if c_new[p[n-1]] == n - 1:
            break
    return p

def gen_suffix_array_and_lcp(s_: str) -> tuple[list[int], list[int]]:
    def radix_sort(p_: list[int], c_: list[int]) -> list[int]:
        count: list[int] = [0 for _ in range(len(p_))]
        for x in p_:
            count[c_[x]] += 1
        new_p: list[int] = p_.copy()
        pos: list[int] = [0 for _ in range(len(p_))]
        for i in range(1, len(p_)):
            pos[i] = pos[i-1] + count[i-1]
        for x in p_:
            new_p[pos[c_[x]]] = x
            pos[c_[x]] += 1
        return new_p
    s_ += "$"
    n: int = len(s_)
    a: list[tuple[str, int]] = [(s_[i], i) for i in range(n)]
    a.sort(key=lambda x: x[0])
    p: list[int] = [a[i][1] for i in range(n)]
    c: list[int] = [0] * n
    c[p[0]] = 0
    for i in range(1, n):
        if a[i][0] == a[i-1][0]:
            c[p[i]] = c[p[i-1]]
        else:
            c[p[i]] = c[p[i-1]] + 1
    k: int = 1
    while (1 << k) <= 2*n:
        p = [(p[i] - (1 << (k-1))) % n for i in range(n)]
        p = radix_sort(p, c)

        c_new: list[int] = [0] * n
        prev: tuple[int, int] = (c[p[0]], c[(p[0] + (1 << (k-1))) % n])
        for i in range(1, n):
            curr: tuple[int, int] = (c[p[i]], c[(p[i] + (1 << (k-1))) % n])
            if prev == curr:
                c_new[p[i]] = c_new[p[i-1]]
            else:
                c_new[p[i]] = c_new[p[i-1]] + 1
            prev = curr
        c = c_new
        k += 1
        if c_new[p[n-1]] == n - 1:
            break

    lcp: list[int] = [0] * (n-1)
    k: int = 0
    for i in range(n-1):
        # i => where do we start (in the string) this suffix. we never start the suffix at n-1.
        # because the suffix at n-1 is $ and it is the first of the suffix array so we don't have a previous suffix to 
        # compare it to.
        pi: int = c[i]  # pi => position of the suffix i in the suffix array.
        # pi is never 0 because the suffix at 0 is $
        j: int = p[pi - 1]  # j => where does the previous (in the suffix array) suffix start (in the string).
        while s_[i+k] == s_[j+k]:
            k += 1
        lcp[pi-1] = k
        k = max(k-1, 0)

    return p, lcp

def get_lps(string: str) -> list[int]:
    lps: list[int] = [0] * len(string)
    length: int = 0
    i: int = 1
    while i < len(string):
        if string[i] == string[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def create_string_hash(string: str, n: int, p: int, mod: int) -> tuple[list[int], list[int]]:
    hash_prefixes: list[int] = [0] * (n + 1)
    powers: list[int] = [1] * (n + 1)
    for i in range(1, n + 1):
        powers[i] = (powers[i - 1] * p) % mod
    for i in range(n):
        hash_prefixes[i + 1] = (hash_prefixes[i] * p + (ord(string[i]) - ord("a") + 1)) % mod
    return hash_prefixes, powers

def get_hash(hash_prefixes: list[int], powers: list[int], mod: int, i: int, j: int) -> int:
    """
    Returns the hash of the substring s[i:j] (j excluded) 
    """
    return (hash_prefixes[j] - hash_prefixes[i] * powers[j-i]) % mod

def make_nCr_mod(max_n: int, mod: int = 10**9+7):
    max_n = min(max_n, mod - 1)

    fact, inv_fact = [0] * (max_n + 1), [0] * (max_n + 1)
    fact[0] = 1
    for i in range(max_n):
        fact[i + 1] = fact[i] * (i + 1) % mod

    inv_fact[-1] = pow(fact[-1], mod - 2, mod)
    for i in reversed(range(max_n)):
        inv_fact[i] = inv_fact[i + 1] * (i + 1) % mod

    def nCr_mod(n, r):
        res = 1
        while n or r:
            a, b = n % mod, r % mod
            if a < b:
                return 0
            res = res * fact[a] % mod * inv_fact[b] % mod * inv_fact[a - b] % mod
            n //= mod
            r //= mod
        return res

    return nCr_mod

def sum_from_k_to_n(k_: int, n_: int) -> int:
    # k inclusive, n inclusive
    return (n_ * (n_ + 1) - k_ * (k_ - 1)) // 2

class FenwickTree:
    def __init__(self, x):
        bit = self.bit = list(x)
        size = self.size = len(bit)
        for i in range(size):
            j = i | (i + 1)
            if j < size:
                bit[j] += bit[i]

    def update(self, idx, x):
        """updates bit[idx] += x"""
        while idx < self.size:
            self.bit[idx] += x
            idx |= idx + 1

    def __call__(self, end):
        """calc sum(bit[:end])"""
        x = 0
        while end:
            x += self.bit[end - 1]
            end &= end - 1
        return x

    def find_kth(self, k):
        """Find largest idx such that sum(bit[:idx]) <= k"""
        idx = -1
        for d in reversed(range(self.size.bit_length())):
            right_idx = idx + (1 << d)
            if right_idx < self.size and self.bit[right_idx] <= k:
                idx = right_idx
                k -= self.bit[idx]
        return idx + 1, k
    
class SortedList:
    block_size = 700

    def __init__(self, iterable=()):
        self.macro = []
        self.micros = [[]]
        self.micro_size = [0]
        self.fenwick = FenwickTree([0])
        self.size = 0
        for item in iterable:
            self.insert(item)

    def insert(self, x):
        i = lower_bound(self.macro, x)
        j = upper_bound(self.micros[i], x)
        self.micros[i].insert(j, x)
        self.size += 1
        self.micro_size[i] += 1
        self.fenwick.update(i, 1)
        if len(self.micros[i]) >= self.block_size:
            self.micros[i:i + 1] = self.micros[i][:self.block_size >> 1], self.micros[i][self.block_size >> 1:]
            self.micro_size[i:i + 1] = self.block_size >> 1, self.block_size >> 1
            self.fenwick = FenwickTree(self.micro_size)
            self.macro.insert(i, self.micros[i + 1][0])

    def pop(self, k=-1):
        i, j = self._find_kth(k)
        self.size -= 1
        self.micro_size[i] -= 1
        self.fenwick.update(i, -1)
        return self.micros[i].pop(j)

    def __getitem__(self, k):
        i, j = self._find_kth(k)
        return self.micros[i][j]

    def count(self, x):
        return self.upper_bound(x) - self.lower_bound(x)

    def __contains__(self, x):
        return self.count(x) > 0

    def lower_bound(self, x):
        i = lower_bound(self.macro, x)
        return self.fenwick(i) + lower_bound(self.micros[i], x)

    def upper_bound(self, x):
        i = upper_bound(self.macro, x)
        return self.fenwick(i) + upper_bound(self.micros[i], x)

    def _find_kth(self, k):
        return self.fenwick.find_kth(k + self.size if k < 0 else k)

    def __len__(self):
        return self.size

    def __iter__(self):
        return (x for micro in self.micros for x in micro)

    def __repr__(self):
        return str(list(self))

class SqrtDecomposition:
    def __init__(self, initial_array=None):
        # Initialize the array and build the blocks
        if initial_array is None:
            initial_array = []
        self.arr: list[int] = initial_array
        self.n: int = len(self.arr)
        self.block_size: int = int(math.sqrt(self.n)) if self.n > 0 else 10  # The blocks themselves
        self.block_sizes: list[int] = []  # To track the dynamic sizes of the blocks
        self.blocks: list[list[int]] = []
        self.lazy: list[int] = []
        for i in range(0, self.n, self.block_size):
            # Last block won't have an error because when you slice a list, it doesn't throw an error if the end index
            # is out of bounds, it just returns the elements up to the last index.
            block = self.arr[i:i + self.block_size]
            self.block_sizes.append(len(block))
            self.blocks.append(block)
            self.lazy.append(0)

    def _apply_lazy(self, block_idx: int) -> None:
        """
        Apply lazy updates to the block before accessing it.
        """
        if self.lazy[block_idx] != 0:
            # Apply the cached lazy update to the block
            for i in range(len(self.blocks[block_idx])):
                self.blocks[block_idx][i] += self.lazy[block_idx]
            # Clear the lazy value
            self.lazy[block_idx] = 0

    def _find_block(self, idx: int) -> tuple[int, int]:
        """
        Find the block index corresponding to a global index idx.
        """
        sum_size = 0
        for i, size in enumerate(self.block_sizes):
            if sum_size + size > idx:
                return i, idx - sum_size  # Block index and offset inside block
            sum_size += size
        return -1, -1  # In case idx is out of bounds

    def _split_block(self, block_idx):
        """
        Split a block if it exceeds block_size.
        """
        block = self.blocks[block_idx]
        if len(block) > self.block_size:
            mid = len(block) // 2
            new_block = block[mid:]
            self.blocks[block_idx] = block[:mid]
            self.blocks.insert(block_idx + 1, new_block)
            # Insert corresponding lazy values
            self.lazy.insert(block_idx + 1, 0)
            # Update the block sizes
            self.block_sizes[block_idx] = len(self.blocks[block_idx])
            self.block_sizes.insert(block_idx + 1, len(new_block))

    def insert(self, idx, value):
        """
        Insert an element at index idx.
        """
        if idx == self.n:
            # Insert at the end
            block_idx = len(self.blocks) - 1
            if block_idx == -1:
                # No blocks exist yet
                self.blocks.append([value])
                self.block_sizes.append(1)
                self.lazy.append(0)
                self.n += 1
            else:
                self.blocks[block_idx].append(value)
                self.block_sizes[block_idx] += 1
                self.n += 1
                # If the block size exceeds the threshold, split the block
                self._split_block(block_idx)
                # Rebuild the blocks if necessary
                if len(self.blocks) > 2 * self.block_size:
                    # It means we have 2 times floor(sqrt(n)) blocks, that's too much
                    self._rebuild()
        else:
            # Find right block
            block_idx, offset = self._find_block(idx)
            if block_idx == -1:
                raise IndexError("Index out of bounds")

            self.insert_into_block(block_idx, offset, value)

    def insert_into_block(self, block_idx: int, offset: int, value: int) -> None:
        """
        Used by insert() but can also be used if we already know the block index and offset (with binary search
        if we have sorted arrays for example).
        """
        # Apply lazy updates to the block before insertion
        self._apply_lazy(block_idx)

        # Insert the value and update the block size
        self.blocks[block_idx].insert(offset, value)
        self.block_sizes[block_idx] += 1

        # If the block size exceeds the threshold, split the block
        self._split_block(block_idx)

        # Update the size and rebuild the blocks if necessary
        self.n += 1
        if len(self.blocks) > 2 * self.block_size:
            # It means we have 2 times floor(sqrt(n)) blocks, that's too much
            self._rebuild()

    def _rebuild(self):
        """
        Rebuild the entire block structure if the number of blocks exceeds a threshold.
        """
        new_array = []
        for i, block in enumerate(self.blocks):
            # Apply lazy updates before rebuilding
            self._apply_lazy(i)
            new_array.extend(block)
        self.arr = new_array
        self.n = len(self.arr)
        self.block_size = int(math.sqrt(self.n))
        self.block_sizes = []
        self.blocks = []
        self.lazy = []
        for i in range(0, self.n, self.block_size):
            # Last block won't have an error because when you slice a list, it doesn't throw an error if the end index
            # is out of bounds, it just returns the elements up to the last index.
            block = self.arr[i:i + self.block_size]
            self.block_sizes.append(len(block))
            self.blocks.append(block)
            self.lazy.append(0)

    def range_update(self, left, right, value):
        """
        Add 'value' to all elements in the range [l, r] (both included!).
        """
        start_block, start_offset = self._find_block(left)
        end_block, end_offset = self._find_block(right)

        if start_block == -1 or end_block == -1:
            raise IndexError("Range out of bounds")

        # Apply lazy updates to both start and end blocks if they're partially covered
        self._apply_lazy(start_block)
        self._apply_lazy(end_block)

        if start_block == end_block:
            # Update within the same block
            for i in range(start_offset, end_offset + 1):
                self.blocks[start_block][i] += value
        else:
            # Update the first partial block
            for i in range(start_offset, len(self.blocks[start_block])):
                self.blocks[start_block][i] += value

            # Update the full blocks in between
            for i in range(start_block + 1, end_block):
                self.lazy[i] += value  # Mark these blocks as lazy

            # Update the last partial block
            for i in range(0, end_offset + 1):
                self.blocks[end_block][i] += value

    def query(self, idx):
        """
        Return the value at index idx (applying any pending lazy updates).
        """
        block_idx, offset = self._find_block(idx)
        if block_idx == -1:
            raise IndexError("Index out of bounds")
        self._apply_lazy(block_idx)
        return self.blocks[block_idx][offset]

    def display(self):
        """
        Helper function to display the current state of the blocks and lazy.
        """
        print("Blocks:")
        for i, block in enumerate(self.blocks):
            print(f"Block {i}: {block}, Lazy: {self.lazy[i]}")

    def find_index_to_insert(self, value: int) -> tuple[int, int]:
        """
        Find the index (rightmost) where the value should be inserted in the array IF THE UNDERLYING ARRAY IS SORTED.
        This is not necessarily the case, this class can work with unsorted arrays.
        Returns block number AND index within the block.
        """
        # Binary search to find the block
        left, right = 0, len(self.blocks) - 1
        while left < right:
            mid = (left + right) // 2
            # Relax block first
            self._apply_lazy(mid)
            if self.blocks[mid][-1] <= value:
                left = mid + 1
            else:
                # It means self.blocks[mid][-1] > value
                right = mid
        block_idx = left
        # Relax block first
        self._apply_lazy(left)
        # Binary search within the block
        block = self.blocks[block_idx]
        left, right = 0, len(block)
        while left < right:
            mid = (left + right) // 2
            if block[mid] <= value:
                left = mid + 1
            else:
                # It means block[mid] > value
                right = mid
        return block_idx, left