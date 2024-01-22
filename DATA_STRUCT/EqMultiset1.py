#CSES Concert Tickets
#Construire arbre, faire appels à upper_bound, supprimer éléments

from bisect import bisect_right

SPLIT_SIZE = 2000

input()
prices = sorted(map(int, input().split()))
prices = [prices[pos: pos + SPLIT_SIZE] for pos in range(0, len(prices), SPLIT_SIZE)]
splits = [p[0] for p in prices]

for offer in map(int, input().split()):
    split = bisect_right(splits, offer) - 1
    if split == -1:
        print(-1)
        continue
    prices_split = prices[split]
    index = bisect_right(prices_split, offer) - 1
    print(prices_split.pop(index))
    if len(prices_split) == 0:
        del splits[split]
        del prices[split]
    elif index == 0:
        splits[split] = prices_split[0]

# D. Buying gifts
# https://codeforces.com/contest/1802/problem/D

from bisect import bisect
SPLIT_SIZE = 2000

def main():
    for _ in range(int(input())):
        n = int(input())
        a, b = [], []
        for _ in range(n):
            x, y = map(int,input().split())
            a.append(x)
            b.append(y)
        tree, splits = [], []
        for pos, e in enumerate(sorted(b)):
            if pos % SPLIT_SIZE == 0:
                tree.append([e])
                splits.append(e)
            else:
                tree[-1].append(e)

        order = sorted(range(n), key=lambda i:a[i], reverse=True)
        ans = 1<<59
        cmax = -1<<59

        for k in range(n):
            i = order[k]
            ai, bi = a[i], b[i]
            if k != 0:
                cmax = max(cmax, b[order[k-1]])
            ans = min(ans, abs(ai - cmax))

            # REMOVE ELEMENT bi
            split = bisect(splits, bi) - 1
            tree_split = tree[split]
            index = bisect(tree_split, bi) - 1
            tree_split.pop(index)
            if len(tree_split) == 0:
                del splits[split]
                del tree[split]
            elif index == 0:
                splits[split] = tree_split[0]
            
            # SEARCH SPLIT ai
            split = bisect(splits, ai) - 1
            if split == -1:
                # splits[0] is upper_bound
                if splits and splits[0] > cmax:
                    ans = min(ans, abs(ai - splits[0]))
                continue

            #GET LOWER_BOUND
            tree_split = tree[split]
            index = bisect(tree_split, ai) - 1

            if index == -1:
                # tree_split[0] is upper_bound
                if tree_split and tree_split[0] > cmax:
                    ans = min(ans, abs(ai - tree_split[0]))
                continue
            
            aj_min = tree_split[index]

            #GET UPPER_BOUND
            aj_max = None
            if index + 1 < len(tree_split):
                aj_max = tree_split[index + 1]
            elif split + 1 < len(tree):
                aj_max = tree[split + 1][0]

            if aj_min > cmax:
                ans = min(ans, abs(ai - aj_min))
            if aj_max and aj_max > cmax:
                ans = min(ans, abs(ai - aj_max))

        print(ans)

main()