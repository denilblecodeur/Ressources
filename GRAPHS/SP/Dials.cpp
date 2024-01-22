/*
Dial's algorithm - O(V * lim + E)
Faster than dijkstra for graphs with weights <= 10

test problem : https://www.spoj.com/problems/ADATRIP/
*/

constexpr int lim = 10;
using pii = pair<int, int>;

int n, m, st, dist[20'001];
vector<pii> adj[20'001];

int main() {
	fastio;
	// input
	cin >> n >> m >> st;
	for (int i = 0; i < m; i++) {
		int a, b, c; cin >> a >> b >> c;
		adj[a].push_back({b, c});
	}

	// dial's algorithm
	fill(dist, dist + n + 1, -1);
	vector<vector<int>> Qs(lim + 1);
	dist[st] = 0; Qs[0].push_back(st);
	for (int d = 0, mx = 0; d <= mx; d++) {
		for (auto& Q = Qs[d % (lim + 1)]; Q.size();) {
			int cur = Q.back(); Q.pop_back();
			if (dist[cur] != d) continue;
			for (const auto& [nxt, cost] : adj[cur]) {
				if (dist[nxt] == -1 || dist[nxt] > d + cost) {
					dist[nxt] = d + cost;
					Qs[dist[nxt] % (lim + 1)].push_back(nxt);
					mx = max(mx, dist[nxt]);
				}
			}
		}
	}

	// output
	for (int i = 1; i <= n; i++) {
		if (dist[i] == -1) cout << "INF" << '\n';
		else cout << dist[i] << '\n';
	}
}