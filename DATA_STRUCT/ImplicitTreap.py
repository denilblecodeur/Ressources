from operator import add
from typing import Generic, TypeVar
from collections.abc import Iterator, Callable

S = TypeVar('S')
T = TypeVar('T')

class ImplicitTreap(Generic[S, T]):
    __slots__ = ['root', 'op', 'e', 'mapping', 'composition', 'id', 'val', 'pri', 'ptr', 'cnt', 'acc', 'laz', 'rand']

    def __init__(self, op: Callable[[S, S], S], e: S, mapping: Callable[[T, S], S], composition: Callable[[T, T], T], id: T) -> None:
        self.root = 0
        self.op = op
        self.e = e
        self.mapping = mapping
        self.composition = composition
        self.id = id
        self.val: list[S] = [e]
        self.pri: list[int] = [1 << 32]
        self.ptr: list[int] = [0, 0, 0]
        self.cnt: list[int] = [0]
        self.acc: list[S] = [e]
        #self.laz: list[T] = [id]
        self.rand = self.__xor64()

    def __xor64(self) -> Iterator[int]:
        x = 88172645463325252
        while True:
            x = x ^ ((x << 7) & 0xffffffff)
            x = x ^ (x >> 9)
            yield x & 0xffffffff

    def __newnode(self, x: S) -> int:
        idx = len(self.val)
        self.val.append(x)
        self.pri.append(next(self.rand))
        self.ptr.extend([0, 0, 0])
        self.cnt.append(1)
        self.acc.append(self.e)
        #self.laz.append(self.id)
        return idx

    def __push(self, t: int) -> None:
        #ptr, laz = self.ptr, self.laz
        ptr = self.ptr
        if ptr[t * 3 + 2]:
            ptr[t * 3 + 2] = 0
            l, r = ptr[t * 3], ptr[t * 3 + 1] = ptr[t * 3 + 1], ptr[t * 3]
            if l:
                ptr[l * 3 + 2] ^= 1
            if r:
                ptr[r * 3 + 2] ^= 1
        #if laz[t] != self.id:
        #    l, r = ptr[t * 3], ptr[t * 3 + 1]
        #    acc, val = self.acc, self.val
        #    if l:
        #        laz[l] = self.composition(laz[t], laz[l])
        #        acc[l] = self.mapping(laz[t], acc[l])
        #    if r:
        #        laz[r] = self.composition(laz[t], laz[r])
        #        acc[r] = self.mapping(laz[t], acc[r])
        #    val[t] = self.mapping(laz[t], val[t])
        #    laz[t] = self.id

    def __update(self, t: int) -> None:
        ptr, cnt, acc, val, op = self.ptr, self.cnt, self.acc, self.val, self.op
        l, r = ptr[t * 3], ptr[t * 3 + 1]
        cnt[t] = cnt[l] + cnt[r] + 1
        acc[t] = op(op(acc[l], val[t]), acc[r])

    def __split(self, t: int, k: int, update: bool = False) -> tuple[int, int]:
        ptr, cnt = self.ptr, self.cnt
        l = r = 0
        while t:
            self.__push(t)
            p = cnt[ptr[t * 3]] + 1
            if k < p:
                v, ptr[t * 3] = ptr[t * 3], r
                r, t = t, v
            else:
                v, ptr[t * 3 + 1] = ptr[t * 3 + 1], l
                l, t = t, v
                k -= p
        s = 0
        while l:
            v, ptr[l * 3 + 1] = ptr[l * 3 + 1], s
            if update:
                self.__update(l)
            s, l = l, v
        l = s
        s = 0
        while r:
            v, ptr[r * 3] = ptr[r * 3], s
            if update:
                self.__update(r)
            s, r = r, v
        r = s
        return l, r

    def __merge(self, l: int, r: int, push_lt: bool = False, push_rt: bool = False) -> int:
        ptr, pri = self.ptr, self.pri
        s = 0
        while l:
            if push_lt:
                self.__push(l)
            v, ptr[l * 3 + 1] = ptr[l * 3 + 1], s
            s, l = l, v
        l = s
        s = 0
        while r:
            if push_rt:
                self.__push(r)
            v, ptr[r * 3] = ptr[r * 3], s
            s, r = r, v
        r = s
        t = 0
        while l or r:
            if pri[l] < pri[r]:
                v, ptr[l * 3 + 1] = ptr[l * 3 + 1], t
                self.__update(l)
                t, l = l, v
            else:
                v, ptr[r * 3] = ptr[r * 3], t
                self.__update(r)
                t, r = r, v
        return t

    def build(self, arr):
        n = len(arr)
        val = self.val = [self.e] + arr
        pri = self.pri = [1 << 32] + [next(self.rand) for _ in range(n)]
        ptr = self.ptr = [0] * (n * 3 + 3)
        cnt = self.cnt = [0] + [1] * n
        acc = self.acc = [self.e] * (n + 1)
        #laz = self.laz = [self.id] * (n + 1)
        op = self.op
        par = [0] * (n + 1)
        for i in range(2, n + 1):
            p = i - 1
            l = 0
            while p and pri[i] > pri[p]:
                pp = par[p]
                if l:
                    par[l] = p
                par[p] = i
                l, p = p, pp
            par[i] = p
        for i, p in enumerate(par):
            if not p:
                self.root = i
            elif i < p:
                ptr[p * 3] = i
            else:
                ptr[p * 3 + 1] = i
        stack = [self.root]
        ord = []
        while stack:
            v = stack.pop()
            ord.append(v)
            l, r = ptr[v * 3], ptr[v * 3 + 1]
            if l:
                stack.append(l)
            if r:
                stack.append(r)
        for v in ord[::-1]:
            l, r = ptr[v * 3], ptr[v * 3 + 1]
            cnt[v] = cnt[l] + cnt[r] + 1
            acc[v] = op(op(acc[l], val[v]), acc[r])

    def size(self) -> int:
        return self.cnt[self.root]

    def insert(self, pos: int, x: S) -> None:
        l, r = self.__split(self.root, pos)
        self.root = self.__merge(self.__merge(l, self.__newnode(x)), r)

    def erase(self, pos: int) -> None:
        l, r = self.__split(self.root, pos + 1)
        l, _ = self.__split(l, pos)
        self.root = self.__merge(l, r)

    def get(self, pos: int) -> S:
        t1, t2 = self.__split(self.root, pos + 1, True)
        t1, t3 = self.__split(t1, pos, True)
        res = self.val[t3]
        self.root = self.__merge(self.__merge(t1, t3), t2)
        return res

    def reverse(self, l: int, r: int) -> None:
        t2, t3 = self.__split(self.root, r)
        t1, t2 = self.__split(t2, l)
        self.ptr[t2 * 3 + 2] ^= 1
        self.root = self.__merge(self.__merge(t1, t2, False, True), t3, True, False)

    #def apply(self, l: int, r: int, x: T) -> None:
    #    t2, t3 = self.__split(self.root, r)
    #    t1, t2 = self.__split(t2, l)
    #    self.laz[t2] = self.composition(x, self.laz[t2])
    #    self.root = self.__merge(self.__merge(t1, t2, False, True), t3, True, False)

    def prod(self, l: int, r: int) -> S:
        t2, t3 = self.__split(self.root, r, True)
        t1, t2 = self.__split(t2, l, True)
        res = self.acc[t2]
        self.root = self.__merge(self.__merge(t1, t2), t3)
        return res

    def iter(self) -> Iterator[S]:
        stack = []
        v = self.root
        while stack or v:
            while v:
                self.__push(v)
                stack.append(v)
                v = self.ptr[v * 3]
            v = stack.pop()
            yield self.val[v]
            v = self.ptr[v * 3 + 1]

seq = ImplicitTreap(add, 0, lambda x, a: x, lambda x, a: x, 0)
"""
seq.build(A)
seq.reverse(l, r) # [l,r) 0-indexed
ret = seq.prod(l, r) # [l,r) 0-indexed
"""