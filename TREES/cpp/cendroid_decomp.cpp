vvi adj;
vector<bool> isrem;
vi subsz;

/** DFS to calculate the size of the subtree rooted at `node` */
int get_subsz(int v, int p = -1) {
	subsz[v] = 1;
	for (int u : adj[v]) {
		if (u == p || isrem[u]) { continue; }
		subsz[v] += get_subsz(u, v);
	}
	return subsz[v];
}

/**
 * Returns a centroid (a tree may have two centroids) of the subtree
 * containing node `node` after node removals
 * @param v current node
 * @param tsz size of current subtree after node removals
 * @param p parent of u
 * @return first centroid found
 */
int get_centroid(int v, int tsz, int p = -1) {
	for (int u : adj[v]) {
		if (u == p || isrem[u]) continue;
		if (subsz[u] * 2 > tsz) {
			return get_centroid(u, tsz, v);
		}
	}
	return v;
}

/** Build up the centroid decomposition recursively */
void build_cd(int v = 0) {
	int centroid = get_centroid(v, get_subsz(v));

	// do something

	isrem[centroid] = true;

	for (int u : adj[centroid]) {
		if (isrem[u]) continue;
		build_cd(u);
	}
}