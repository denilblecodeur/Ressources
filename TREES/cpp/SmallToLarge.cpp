#include <bits/stdc++.h>
#define endl '\n'
#define fastio ios::sync_with_stdio(false), cout.tie(nullptr), cin.tie(nullptr);
using namespace std;

struct Query{
    int i, l, r;
};

void merge(set<int>& s, set<int>& t) {
	if (s.size() < t.size())
		s.swap(t);
	for (auto x : t)
		s.insert(x);
	t = {};
}

void solve(){
    int N, Q;
    cin >> N >> Q;
    vector<vector<int>> adj(N + 1);
    for(int i=0; i<N-1; i++){
        int u, v; cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> p(N + 1);
    for(int i=1; i<=N; i++){
        int j; cin >> j;
        p[j] = i;
    }
    vector<char> ans(Q);
    vector<vector<Query>> query(N + 1);
    vector<set<int>> vset(N + 1);
    for(int i=0; i<Q; i++){
        int l, r, x; cin >> l >> r >> x;
        query[x].push_back({i, l, r});
    }
    auto dfs = [&](auto self, int v, int par) -> void {
        for(int u : adj[v]){
            if(u == par) continue;
            self(self, u, v);
            merge(vset[v], vset[u]);
        }
        vset[v].insert(p[v]);
        for(auto T : query[v]){
            auto[i, l, r] = T;
            auto it = vset[v].lower_bound(l);
			ans[i] = it != vset[v].end() && *it <= r;
        }
	};
    dfs(dfs, 1, 0);
    for (auto c : ans) cout << (c ? "YES" : "NO") << endl;
}

int main(){
    fastio;
    int t; cin >> t;
    while(t--){
        solve();
    }
}