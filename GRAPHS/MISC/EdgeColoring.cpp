// O(V.E) Misra & Gries edge coloring algorithm
// Given a simple, undirected graph with max degree D,
// computes (D + 1)-coloring of the edges such that no neighboring edges share a color
vi edgeColoring(int N, vector<pii> eds) {
	vi cc(N + 1), ret((int)(eds).size()), fan(N), free(N), loc;
	for (pii e : eds) ++cc[e.first], ++cc[e.second];
	int u, v, ncols = *max_element(cc.begin(), cc.end()) + 1;
	vector<vi> adj(N, vi(ncols, -1));
	for (pii e : eds) {
		tie(u, v) = e;
		fan[0] = v;
		loc.assign(ncols, 0);
		int at = u, end = u, d, c = free[u], ind = 0, i = 0;
		while (d = free[v], !loc[d] && (v = adj[u][d]) != -1)
			loc[d] = ++ind, cc[ind] = d, fan[ind] = v;
		cc[loc[d]] = c;
		for (int cd = d; at != -1; cd ^= c ^ d, at = adj[at][cd])
			swap(adj[at][cd], adj[end = at][cd ^ c ^ d]);
		while (adj[fan[i]][d] != -1) {
			int left = fan[i], right = fan[++i], e = cc[i];
			adj[u][e] = left;
			adj[left][e] = u;
			adj[right][e] = -1;
			free[right] = e;
		}
		adj[u][d] = fan[i];
		adj[fan[i]][d] = u;
		for (int y : {fan[0], u, end})
			for (int& z = free[y] = 0; adj[y][z] != -1; z++);
	}
	for(int i=0; i<(int)(eds).size(); i++){
		for (tie(u, v) = eds[i]; adj[u][ret[i]] != v;) ++ret[i];
    }
	return ret;
}

int main(){
    int n, m; cin >> n >> m;
    vector<pii> eds;
    for(int i=0; i<n*m; i++){
        int eq1 = i/n;
        for(int j=i+1; j<n*m; j++){
            int eq2 = j/n;
            if(eq1 != eq2){
                eds.pb({i, j});
            }
        }
    }
    vi color = edgeColoring(n*m, eds);
    vector<vpii> ans((m-1)*n+1, vpii());
    for(int i=0; i<eds.size(); i++){
        ans[color[i]].pb(eds[i]);
    }
    for(int i=0; i<(m-1)*n+1; i++){
        int sz = ans[i].size();
        for(int j=0; j<sz; j++){
            auto[x,y] = ans[i][j];
            cout << (char)('A'+x/n) << x%n+1 << '-' << (char)('A'+y/n) << y%n+1 << " \n"[j==sz-1];
        }
    }
}