#Greedy
n = int(input())
p = list(map(int,input().split()))
pos = {v:k for k,v in enumerate(p)}
swaps = 0
for i in range(n):
    if p[i] != i + 1:
        temp = p[i]
        p[i] = i + 1
        p[pos[i + 1]] = temp
        pos[temp] = pos[i + 1]
        pos[i + 1] = i
        swaps += 1
        
print(swaps)

#Graph cycle
n = int(input())
p = list(map(int,input().split()))
visited = [-1] * n
len_cycles = 0
k = 0
for i in sorted(range(n), key=lambda i:p[i]):
    if visited[i] != -1 or p[i] == i + 1:
        continue
    j = i
    cycle_size = 0
    while visited[j] == -1:
        visited[j] = k
        j = p[j] - 1
        cycle_size += 1
    k += 1
    len_cycles += cycle_size - 1
            
print(len_cycles)

"""
len_cycles is the minimum number of swaps to sort the array
To obtain 1 inversion, len_cycles - 1 if k and k+1 in same cycle, else len_cycles + 1
"""