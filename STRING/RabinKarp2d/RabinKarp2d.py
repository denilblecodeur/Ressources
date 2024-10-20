A = 684515155
B = 1000000007
invA = pow(A, -1, B)

def RabinKarp2d(grid, pattern, structurels):
	N1, N2 = len(grid), len(grid[0])
	K1, K2 = len(pattern), len(pattern[0])
	P1 = [[pattern[i][j] if pattern[i][j] in structurels else chr(0) for j in range(K2)] for i in range(K1)]
	G1 = [[grid[i][j] if grid[i][j] in structurels else chr(0) for j in range(N2)] for i in range(N1)]

	refhash = sum(ord(P1[i][j]) * pow(A, K2 * i + j, B) for i in range(K1) for j in range(K2)) % B

	hash1d = []
	for i in range(N1):
		hash1d += [[sum(ord(G1[i][j]) * pow(A, j, B) for j in range(K2)) % B]]
		for j in range(K2, N2):
			hash1d[i] += [((hash1d[i][-1] - ord(G1[i][j - K2])) * invA + ord(G1[i][j]) * pow(A, K2 - 1, B)) % B]

	hash2d = [[0 for j in range(K2, N2 + 1)] for i in range(K1, N1 + 1)]
	for j in range(K2, N2 + 1):
		hash2d[0][j - K2] = sum(hash1d[i][j - K2] * pow(A, i * K2, B) for i in range(K1)) % B
	for i in range(K1, N1):
		for j in range(K2, N2 + 1):
			hash2d[i - K1 + 1][j - K2] = ((hash2d[i - K1][j - K2] - hash1d[i - K1][j - K2]) * pow(invA, K2, B) + hash1d[i][j - K2] * pow(A, K2 * (K1 - 1), B)) % B
			
	matches = []
	for i in range(N1 + 1 - K1):
		for j in range(N2 + 1 - K2):
			if hash2d[i][j] == refhash and P1 == [aux[j:j + K2] for aux in G1[i:i + K1]]:
                # match found
				matches.append((i, j))
	return matches