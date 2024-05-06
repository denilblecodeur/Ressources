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