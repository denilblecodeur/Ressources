class Matrix():
    def __init__(self,A,H,W):
        self._matrix=[]
        if type(A[0])==int:
            self.H=H
            self.W=W
            self._matrix=A
        else:
            self.H=len(A)
            self.W=len(A[0])
            for aa in A:
                self._matrix.extend(aa)

    def __getitem__(self,item):
        H,W,A=self.H,self.W,self._matrix
        if type(item)==tuple:
            i,j=item
            return self._matrix[i*W+j]
        else:
            return self._matrix[item*W:(item+1)*W]

    def __setitem__(self,item,val):
        H,W,A=self.H,self.W,self._matrix
        if type(item)==tuple:
            i,j=item
            self._matrix[i*W+j]=val
        else:
            self._matrix[item*W:(item+1)*W]=val

    def __add__(self,B):
        #assert (self.row,self.column)==(other.row,other.column), "sizes of matrices are different"
        H,W,A=self.H,self.W,self._matrix
        AB=[0]*(H*W)
        for h in range(H):
            for w in range(W):
                AB[h*W+w]=add2(A[h*W+w],B._matrix[h*W+w])
        return Matrix(AB,H,W)

    def __mul__(self,other):
        H,W,A=self.H,self.W,self._matrix
        if type(other)==Vector:
            vec=other
            res=[0]*W
            for i in range(H):
                for j in range(W):
                    res[i]=add2(res[i],mul2(A[i*W+j],vec[j]))
            return Vector(res)
        else:
            # assert self.column!=other.row, "sizes of matrices are different"
            AB=[0]*(other.W*H)
            for i in range(H):
                for j in range(other.W):
                    temp=0
                    for k in range(W):
                        temp=add2(temp,mul2(A[i*W+k],other._matrix[k*other.W+j]))
                    AB[i*other.W+j]=temp
            return Matrix(AB,H,other.W)

    def __truediv__(self,c):
        H,W,A=self.H,self.W,self._matrix
        res=A.copy()
        for h in range(H):
            for w in range(W):
                res[h*W+w]=mul2(res[h*W+w],mul_inv2(c))
        return Matrix(res,H,W)

    def __floordiv__(self,c):
        H,W,A=self.H,self.W,self._matrix
        res=A.copy()
        for h in range(H):
            for w in range(W):
                res[h*W+w]=res[h*W+w]//c
        return Matrix(res,H,W)

    def __mod__(self,c):
        H,W,A=self.H,self.W,self._matrix
        res=A.copy()
        for h in range(H):
            for w in range(W):
                res[h*W+w]=res[h*W+w]%c
        return Matrix(res,H,W)

    def __pow__(self,m):
        # assert self.column==self.row, "the size of row must be the same as that of column"
        H,W,A=self.H,self.W,self._matrix
        if m==0:
            return identity(H)
        else:
            m-=1
            res=self
            while m:
                if m%2==1:
                    res*=self
                self=self*self
                m>>=1
            return res

    def __eq__(self,other):
        if type(other)==Matrix:
            return self._matrix==other._matrix
        return False

    def __ne__(self,other):
        if type(other)==Matrix:
            return self._matrix!=other._matrix
        return True

    def __len__(self):
        return self.H

    def __str__(self):
        H,W,A=self.H,self.W,self._matrix
        res=[]
        for i in range(self.H):
            for j in range(self.W):
                res.append(str(self._matrix[i*W+j]))
                res.append(" ")
            res.append("\n")
        return "".join(res)

    def __hash__(self):
        H,W,A=self.H,self.W,self._matrix
        res=[]
        for h in range(self.H):
            for w in range(self.W):
                res.append(self._matrix[h*W+w])
        return tuple(res)

    def det(self):
        H,W,A=self.H,self.W,self._matrix
        n=H
        res=1
        for i in range(n):
            if A[i*W+i]==0:
                res=add_inv2(res)
                for k in range(i+1,n):
                    if A[k*W+i]!=0:
                        for w in range(W):
                            A[i*W+w],A[k*W+w]=A[k*W+w],A[i*W+w]
                        break
                else:
                    return 0
            c=mul_inv2(A[i*W+i])
            for j in range(i+1,n):
                l=mul2(c,A[j*W+i])
                for k in range(i+1,n):
                    A[j*W+k]=add2(A[j*W+k],add_inv2(l*A[i*W+k]))
        for i in range(n):
            res=mul2(res,A[i*W+i])
        return res

    def map(self,func):  # act func to all elements
        H,W,A=self.H,self.W,self._matrix
        res=A.copy()
        for h in range(H):
            for w in range(W):
                res[h*W+w]=func(res[h*W+w])
        return Matrix(res,H,W)


    def count(self,x):
        H,W,A=self.H,self.W,self._matrix
        cnt=0
        for h in range(self.H):
            for w in range(self.W):
                cnt+=(self._matrix[h*W+w]==x)
        return cnt

    def rank(self):
        """ = dimension"""
        H,W,A=self.H,self.W,self._matrix
        A=A[:]
        rank=0
        p,q=[],[]
        for w in range(W):
            for h in range(rank,H):
                if A[h*W+w]!=0:
                    break
            else:
                q.append(w)
                continue
            if w==W: return -1,[],[]
            p.append(w)
            for ww in range(W):
                A[rank*W+ww],A[h*W+ww]=A[h*W+ww],A[rank*W+ww]
            inv=mul_inv2(A[rank*W+w])
            for ww in range(W):
                A[rank*W+ww]=mul2(A[rank*W+ww],inv)
            for h in range(H):
                if h==rank: continue
                c=add_inv2(A[h*W+w])
                for ww in range(W):
                    A[h*W+ww]=add2(A[h*W+ww],mul2(c,A[rank*W+ww]))
            rank+=1
        return rank

class Vector():
    def __init__(self,vec):
        self.n=len(vec)
        self._vector=vec

    def __getitem__(self,item):
        return self._vector[item]

    def __setitem__(self,item,val):
        self._vector[item]=val

    def __neg__(self):
        n,vec=self.n,self._vector
        res=[]
        for x in vec:
            res.append(add_inv2(x))
        return Vector(res)

    def __add__(self,vec2):
        n,vec=self.n,self._vector
        res=vec.copy()
        for i in range(n):
            res[i]=add2(res[i],vec2[i])
        return Vector(res)

    def __sub__(self,vec2):
        n,vec=self.n,self._vector
        res=vec.copy()
        for i in range(n):
            res[i]=add2(res[i],add_inv2(vec2[i]))
        return Vector(res)

    def __mul__(self,vec2):
        n,vec=self.n,self._vector
        if type(vec2)!=int:
            res=vec.copy()
            for i in range(n):
                res[i]=mul2(res[i],vec2[i])
            return Vector(res)
        else:
            res=[mul2(vec2,vec[i]) for i in range(n)]
            return Vector(res)

    def __truediv__(self,c):
        n,vec=self.n,self._vector
        res=vec.copy()
        for i in range(n):
            res[i]=mul2(res[i],mul_inv2(c))
        return Vector(res)

    def __floordiv__(self,c):
        n,vec=self.n,self._vector
        res=vec.copy()
        for i in range(n):
            res[i]=res[i]//c
        return Vector(res)

    def __mod__(self,c):
        n,vec=self.n,self._vector
        res=vec.copy()
        for i in range(n):
            res[i]=res[i]%c
        return Vector(res)

    def map(self,func):  # act func to all elements
        n,vec=self.n,self._vector
        res=vec.copy()
        for i in range(n):
            res[i]=func(res[i])
        return Vector(res)

    def __eq__(self,other):
        if type(other)==Vector:
            return self._vector==other._vector
        return False

    def __ne__(self,other):
        if type(other)==Vector:
            return self._vector!=other._vector
        return True

    def __len__(self):
        return self.n

    def __str__(self):
        res=[]
        for i in range(self.n):
            res.append(str(self._vector[i]))
            res.append(" ")
        return "".join(res)

    def __hash__(self):
        return tuple(self._vector)

    def count(self,x):
        cnt=0
        for a in self._vector:
            cnt+=(a==x)
        return cnt


def linear_equations(mat, vec):
    """
    return
        (dim, [x,y,z], [[a0,b0,c0],[a1,b1,c1],...])

    which means,

        solution = (x,y,z)+t0*(a0,b0,c0)+t1*(a1,b1,c1)+...

    Cation: float
    """
    if type(mat) is Matrix:
        H,W=mat.H,mat.W
    else:
        H, W = len(mat), len(mat[0])
    # assert H == len(vec)
    aug=[]
    for h in range(H):
        aug.extend(mat[h]+[vec[h]])
    rank = 0
    p,q = [],[]
    W2=W+1
    for w in range(W + 1):
        for h in range(rank, H):
            if aug[h*W2+w] != 0:
                break
        else:
            q.append(w)
            continue
        if w == W: return -1, [], []
        p.append(w)
        for ww in range(W+1):
            aug[rank*W2+ww], aug[h*W2+ww] = aug[h*W2+ww], aug[rank*W2+ww]
        inv = mul_inv2(aug[rank*W2+w])
        for ww in range(W + 1):
            aug[rank*W2+ww] = mul2(aug[rank*W2+ww], inv)
        for h in range(H):
            if h == rank: continue
            c = add_inv2(aug[h*W2+w])
            for ww in range(W + 1):
                aug[h*W2+ww] = add2(aug[h*W2+ww], mul2(c,aug[rank*W2+ww]))
        rank += 1

    dim = W - rank
    sol = [0] * W
    for h in range(rank):
        sol[p[h]] = aug[h*W2+W2-1]
    vecs = [[0] * W for _ in range(dim)]
    for h in range(dim):
        vecs[h][q[h]] = 1
    for h in range(dim):
        for w in range(rank):
            vecs[h][p[w]] = add_inv2(aug[w*W2+q[h]])
    return dim, sol, vecs

###########################################################
def example():
    global input
    example = iter(
        """
2 3
1 2 3
4 5 6
50 122
        """
            .strip().split("\n"))
    input = lambda: next(example)




##　和＆積（MOD有り）　#######################################
MOD=998244353

def mul2(a,b): return a*b%MOD

def add2(a,b): return (a+b)%MOD

def mul_inv2(a): return pow(a,MOD-2,MOD)

def add_inv2(a): return -a%MOD

def identity(n): return Matrix([[int(i==j) for i in range(n)] for j in range(n)])

###########################################################

import sys
input = sys.stdin.readline

# example()

N,M=map(int, input().split())
A=[]
for h in range(N):
    A.append(list(map(int, input().split())))

A=Matrix(A,N,M)

v=list(map(int, input().split()))
v=Vector(v)


dim, sol, vecs = linear_equations(A,v)
print(dim)
print(*sol)
for vec in vecs:
    print(*vec)