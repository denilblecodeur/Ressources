# https://codeforces.com/contest/1697/problem/F

# toujours déclarer TwoSat() avec N+1 !

def tarjan(G):
    SCC, S, P = [], [], []
    Q, state = list(range(len(G))), [0] * len(G)
    while Q:
        node = Q.pop()
        if node < 0:
            d = state[~node] - 1
            if P[-1] > d:
                SCC.append(S[d:])
                del S[d:]; P.pop()
                for v in SCC[-1]:
                    state[v] = -1
        elif state[node] > 0:
            while P[-1] > state[node]:
                P.pop()
        elif state[node] == 0:
            S.append(node)
            P.append(len(S))
            state[node] = len(S)
            Q.append(~node)
            Q.extend(G[node])
    return SCC[::-1]
 
class TwoSat:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(2 * n)]
 
    def _imply(self, x, y):
        self.graph[x].append(y if y >= 0 else 2 * self.n + y)
 
    def either(self, x, y):
        """either x or y must be True"""
        self._imply(~x, y)
        self._imply(~y, x)
 
    def set(self, x):
        """x must be True"""
        self._imply(~x, x)
 
    def implies(self, x, y):
        self.either(~x, y)
 
    def solve(self):
        SCC = tarjan(self.graph)
        order = [0] * (2 * self.n)
        for i, comp in enumerate(SCC):
            for x in comp:
                order[x] = i
        for i in range(self.n):
            if order[i] == order[~i]:
                return False, None
        return True, [+(order[i] > order[~i]) for i in range(self.n)]
 
 
class Helper:
    def __init__(self, i: int): self.i = i
    def __ge__(self, x: int): return self.i * (K+1) + x - 1
    def __lt__(self, x: int): return ~(self >= x)
    def __gt__(self, x: int): return self >= x + 1
    def __le__(self, x: int): return self < x + 1
 
 
out = []
for _ in range(int(input())):
    N, M, K = map(int, input().split())
    A = [Helper(i) for i in range(N)]
    ts = TwoSat(N*(K+1))
 
    for i in range(N):
        ts.set(A[i] >= 1)
        ts.set(A[i] <= K)
 
        for k in range(1, K):
            ts.implies(A[i] < k, A[i] < k+1)
 
        if i < N-1:
            for k in range(1, K+1):
                ts.implies(A[i] >= k, A[i+1] >= k)
 
    for _ in range(M):
        type, *args = map(int, input().split())
        if type == 1:
            i, x = args; i -= 1
            ts.either(A[i] < x, A[i] > x)
        else:
            i, j, x = args
            i -= 1; j -= 1
 
            if type == 2:
                for y in range(1, K+1):
                    if 1 <= x - y <= K:
                        ts.implies(A[i] >= y, A[j] <= x - y)
                        ts.implies(A[j] >= y, A[i] <= x - y)
 
                if x <= K:
                    ts.set(A[i] < x)
                    ts.set(A[j] < x)
 
            elif type == 3:
                for y in range(1, K+1):
                    if 1 <= x - y <= K:
                        ts.implies(A[i] <= y, A[j] >= x - y)
                        ts.implies(A[j] <= y, A[i] >= x - y)
 
                if x > K:
                    ts.set(A[i] >= x - K)
                    ts.set(A[j] >= x - K)
 
    ok, sol = ts.solve()
    if not ok:
        out.append("-1")
    else:
        ans = []
        for i in range(N):
            for k in range(K, 0, -1):
                if sol[A[i] >= k]:
                    ans.append(str(k))
                    break
            else:
                assert False
 
        out.append(" ".join(ans))
 
print("\n".join(out))