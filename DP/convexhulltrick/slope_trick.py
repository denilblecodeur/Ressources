# VOIR https://judge.yosupo.jp/submission/213065

class slope_trick():
    def __init__(self):
        self.L = [10**17]
        self.R = [10**17]
        self.min_f = 0
 
        self.x_left = 0
        self.x_right = 0
 
    def add_right(self,a):
        a -= self.x_left
        l0 = -self.L[0]
        self.min_f  = self.min_f + max(0,l0-a)
        if l0 <= a:
            a += self.x_left
            a -= self.x_right
            heappush(self.R,a)
        else:
            heappush(self.L,-a)
            a = -heappop(self.L)
            a += self.x_left
            a -= self.x_right
            heappush(self.R,a)
 
        #self.min_f  = self.min_f + max(0,l0-a)
 
    def add_left(self,a):
        a -= self.x_right
        r0 = self.R[0]
        self.min_f = self.min_f + max(0,a-r0)
 
        if a <= r0:
            a += self.x_right
            a -= self.x_left
            heappush(self.L,-a)
        else:
            heappush(self.R,a)
            a = heappop(self.R)
            a += self.x_right
            a -= self.x_left
            heappush(self.L,-a)
 
        #self.min_f = self.min_f + max(0,a-r0)
 
    def add_abs(self,a):
        self.add_left(a)
        self.add_right(a)
 
    def change_min_slide(self,a,b):
        self.x_left += a
        self.x_right += b
    
    def get_val(self,x):
        L = [-l+self.x_left for l in self.L]
        L.sort()
        R = [r+self.x_right for r in self.R]
        R.sort()
 
        res = self.min_f
 
        if 0 < L[-1]:
            L = L[::-1]
            n = len(L)
            for i in range(n):
                c0 = L[i]
                c1 = L[i+1]
        
                if c1 <= x <= c0:
                    res += (i+1) * (c0-x)
                    break
                else:
                    res += (i+1) * (c0-c1)
            return res
        elif L[-1] <= x <= R[0]:
            return res
        else:
            n = len(R)
            for i in range(n):
                c0 = R[i]
                c1 = R[i+1]
                if c0 <= x <= c1:
                    res += (i+1) * (x-c0)
                    break
                else:
                    res += (i+1) * (c1-c0)
            return res


class LiChaoTree:
    def __init__(self, points: list[int], inf: int = 1 << 60):
        """最小値(最大値)を求める頂点集合"""
        xs = sorted(set(points)) if points else [0]
        self.n = n = len(xs)
        self.inf = inf
        self.sz = sz = 2 << n.bit_length() if n & (n - 1) else n
        sz2 = self.sz << 1
        self.bl = [0] * sz2
        self.br = [0] * sz2
        self.dat = [(0, inf)] * sz2
        for i in range(n):
            self.bl[sz + i] = self.br[sz + i] = xs[i]
        for i in range(n, self.sz):
            self.bl[sz + i] = self.br[sz + i] = xs[n - 1]
        for i in range(sz - 1, 0, -1):
            self.bl[i] = self.bl[i << 1]
            self.br[i] = self.br[i << 1 | 1]

    def add_line(self, a: int, b: int) -> None:
        """ax+bの直線を追加する"""
        bl, br, dat = self.bl, self.br, self.dat
        idx = 1
        while True:
            a2, b2 = dat[idx]
            l, r = bl[idx], br[idx]
            lv = a2 * l + b2
            rv = a2 * r + b2
            nlv = a * l + b
            nrv = a * r + b
            if (lv <= nlv) == (rv <= nrv):
                if nlv < lv:
                    dat[idx] = (a, b)
                return
            m = br[idx << 1]
            mv = a2 * m + b2
            nmv = a * m + b
            if nmv < mv:
                dat[idx], (a, b) = (a, b), dat[idx]
                lv, nlv = nlv, lv
            idx = (idx << 1) if nlv < lv else (idx << 1 | 1)

    def add_segment(self, a: int, b: int, l: int, r: int) -> None:
        """線分ax+b(l<=x<=r)を追加する"""
        L, R, bl, br = l, r, self.bl, self.br
        st = [1]
        while st:
            idx = st.pop()
            l, r = bl[idx], br[idx]
            if R < l or r < L:
                continue
            if L <= l and r <= R:
                self.add_line(a, b)
                continue
            st += [idx << 1 | 1, idx << 1]

    def query(self, x: int) -> int:
        """座標xにおける直線群の最小値を返す"""
        idx = 1
        a, b = self.dat[idx]
        res = a * x + b
        while idx < self.sz:
            idx <<= 1
            if x > self.br[idx]:
                idx += 1
            a, b = self.dat[idx]
            res = min(res, a * x + b)
        return res


n, q = map(int, input().split())
lines = [tuple(map(int, input().split())) for _ in range(n)]
queries = []
xs = []
for _ in range(q):
    t, *qu = map(int, input().split())
    if t == 0:
        a, b = qu
        queries.append((a, b))
    else:
        x = qu[0]
        xs.append(x)
        queries.append((None, x))
LCT = LiChaoTree(xs)
for a, b in lines:
    LCT.add_line(a, b)
for a, b in queries:
    if a is None:
        print(LCT.query(b))
    else:
        LCT.add_line(a, b)