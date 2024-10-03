# CP ALGORITHM

n = 1000
mex = [None] * (n+1)
mex[0] = 0
mex[1] = 1

def grundyValue(n):
    if mex[n] is not None:
        return mex[n]
    excluded = {grundyValue(n-2)}
    for i in range(2, n):
        excluded.add(grundyValue(i-2) ^ grundyValue(n-i-1))
    res = 0
    while res in excluded:
        res += 1
    mex[n] = res
    return res

grundyValue(n)

"""
ITERATIF
for x in range(2, n+1):
    excluded = {mex[x-2]}
    for i in range(2, x):
        excluded.add(mex[i-2] ^ mex[x-i-1])
    res = 0
    while res in excluded:
        res += 1
    mex[x] = res
"""

for cycle_len in range(2, 100):
    for start in range(n-2*cycle_len):
        if mex[start:start+cycle_len] == mex[start+cycle_len:start+2*cycle_len]:
            print(start, cycle_len)
            exit()

# ISOGRAD

def get_mex(f, d):
	"""
		computes the Minimum EXcluded for a given state
	"""
	if (f, d) not in mem:
		excluded = set()
		children = get_all_children_pair(f,d)
		for new_f, new_d in children:
			excluded.add(get_mex(new_f, new_d))
		res = 0
		while res in excluded:
			res += 1
		mem[(f,d)] = res
	return mem[(f,d)]

mem = dict()
mex = 0
for i in range(N):
    mex ^= get_mex(F[i], D[i])