def compute_extension(a):
    extension = [0]
    ms = [0]
    for i in range(1, len(a)):
        while ms and a[i] <= a[ms[-1]]: ms.pop()
        if ms: extension.append(i - ms[-1] - 1)
        else: extension.append(i)
        ms.append(i)
    return extension

n = int(input())
a = list(map(int,input().split()))

left_extension = compute_extension(a)
right_extension = compute_extension(a[::-1])[::-1]
cover = [a[i] * (r + l + 1) for i, (l, r) in enumerate(zip(left_extension, right_extension))]

print(*left_extension)
print(*right_extension)
print(*cover)
print(max(cover))