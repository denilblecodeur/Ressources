n = int(input())
p = [tuple(map(float,input().split())) for _ in range(n)]
bot, top = convex_hull(p)

i, j = 0, len(bot)-1
ans = -1

while i<len(top)-1 or j>0:
    ans = max(ans, dist(top[i], bot[j]))
    if i==len(top)-1:
        j -= 1
    elif j==0:
        i += 1
    else:
        if (top[i+1][1]-top[i][1]) * (bot[j][0]-bot[j-1][0]) > (bot[j][1]-bot[j-1][1]) * (top[i+1][0]-top[i][0]):
            i += 1
        else:
            j -= 1

print(round(ans))