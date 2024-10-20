"""
À TESTER
class SparseTable:
    __slots__=('n','st','e','mx','op')
    def __init__(self,op,e,arr):#n!=0
        self.n=len(arr)
        self.mx=(self.n-1).bit_length()#取不到
        self.op=op
        self.e=e
        self.st=[0]*(self.n*self.mx)
        for i in range(self.n):
            self.st[i]=arr[i]
        for j in range(1,self.mx):
            for i in range(self.n-(1<<j)+1):
                self.st[j*self.n+i]=op(self.st[i+(j-1)*self.n],self.st[i+(1<<j-1)+(j-1)*self.n])
    def query(self,l,r):
        if l>r:return self.e
        s=(r-l>>1).bit_length()
        return self.op(self.st[s*self.n+l],self.st[r-(1<<s)+1+s*self.n])
"""

class SparseTable:
    def __init__(self, arr, op=min):
        self.op = op
        self.n = len(arr)
        self.h = self.n.bit_length() - 1
        self.table = [[0] * self.n for _ in range(self.h + 1)]
        self.table[0] = [a for a in arr]
        for k in range(self.h):
            nxt, prv = self.table[k + 1], self.table[k]
            l = 1 << k
            for i in range(self.n - l * 2 + 1):
                nxt[i] = op(prv[i], prv[i + l])

    def prod(self, l, r): # [l, r)
        assert 0 <= l < r <= self.n
        k = (r - l).bit_length() - 1
        return self.op(self.table[k][l], self.table[k][r - (1 << k)])

N, Q = map(int, input().split())
A = tuple(map(int, input().split()))

st = SparseTable(A)

res = []

for _ in range(Q):
    l, r = map(int, input().split())
    res.append(A[l - 1] if l == r else st.prod(l - 1, r))

print('\n'.join(map(str, res)))