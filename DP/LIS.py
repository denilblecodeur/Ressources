import bisect

def pathOfLIS(a):
    sub = []
    subIndex = []  
    path = []
    for i, x in enumerate(a):
        if len(sub) == 0 or sub[-1] < x:
            path.append(-1 if len(subIndex) == 0 else subIndex[-1])
            sub.append(x)
            subIndex.append(i)
        else:
            idx = bisect.bisect_left(sub, x) 
            path.append(-1 if idx == 0 else subIndex[idx - 1])
            sub[idx] = x
            subIndex[idx] = i
    ans = []
    t = subIndex[-1]
    while t >= 0:
        ans.append(a[t])
        t = path[t]
    return ans[::-1]



from bisect import bisect

n = int(input())
events = [tuple(map(int,input().split())) for _ in range(n)]
v = int(input())
tot, zero = [], []
for i, e in enumerate(events):
    pos, time = e
    zero.append(abs(pos) <= v * time)
    tot.append((v * time + pos, v * time - pos))
order = sorted(range(n), key=lambda i:tot[i])
lis1, lis2 = [], []
for i in order:
    x, y = tot[i]
    if zero[i]:
        i = bisect(lis1, y)
        if i == len(lis1):
            lis1.append(y)
        else:
            lis1[i] = y
    i = bisect(lis2, y)
    if i == len(lis2):
        lis2.append(y)
    else:
        lis2[i] = y
print(len(lis1), len(lis2))