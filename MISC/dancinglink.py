class dancinglink():
    def __init__(self,n,debug=False):
        self.n = n
        self.debug = debug
        self._left = [i-1 for i in range(n)]
        self._right = [i+1 for i in range(n)]
        self.exist = [True for i in range(n)]
 
    def pop(self,k):
        if self.debug:
            assert self.exist[k]
        L = self._left[k]
        R = self._right[k]
        if L!=-1:
            if R!=self.n:
                self._right[L],self._left[R] = R,L
            else:
                self._right[L] = self.n
        elif R!=self.n:
            self._left[R] = -1
        self.exist[k] = False
 
    def left(self,idx,k=1):
        if self.debug:
            assert self.exist[idx]
        res = idx
        while k:
            res = self._left[res]
            if res==-1:
                break
            k -= 1
        return res
 
    def right(self,idx,k=1):
        if self.debug:
            assert self.exist[idx]
        res = idx
        while k:
            res = self._right[res]
            if res==self.n:
                break
            k -= 1
        return res