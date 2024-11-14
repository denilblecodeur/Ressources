#define DEBUG 1
#include <bits/stdc++.h>
//#include <bits/extc++.h>
#define fastio ios::sync_with_stdio(false), cout.tie(nullptr), cin.tie(nullptr);
using namespace std;

#if DEBUG
// basic debugging macros
int __i__,__j__;
#define printLine(l) for(__i__=0;__i__<l;__i__++){cout<<"-";}cout<<endl
#define printLine2(l,c) for(__i__=0;__i__<l;__i__++){cout<<c;}cout<<endl
#define printVar(n) cout<<#n<<": "<<n<<endl
#define printArr(a,l) cout<<#a<<": ";for(__i__=0;__i__<l;__i__++){cout<<a[__i__]<<" ";}cout<<endl
#define print2dArr(a,r,c) cout<<#a<<":\n";for(__i__=0;__i__<r;__i__++){for(__j__=0;__j__<c;__j__++){cout<<a[__i__][__j__]<<" ";}cout<<endl;}
#define print2dArr2(a,r,c,l) cout<<#a<<":\n";for(__i__=0;__i__<r;__i__++){for(__j__=0;__j__<c;__j__++){cout<<setw(l)<<setfill(' ')<<a[__i__][__j__]<<" ";}cout<<endl;}

// advanced debugging class
// debug 1,2,'A',"test";
class _Debug {
    public:
        template<typename T>
        _Debug& operator,(T val) {
            cout << val << endl;
            return *this;
        }
};
#define debug _Debug(),
#else
#define printLine(l)
#define printLine2(l,c)
#define printVar(n)
#define printArr(a,l)
#define print2dArr(a,r,c)
#define print2dArr2(a,r,c,l)
#define debug
#endif

// define
#define endl '\n'
#define MAX_VAL 999999999
#define MAX_VAL_2 999999999999999999LL
#define EPS 1e-6
#define mp make_pair
#define pb push_back
#define eb emplace_back
#define rep(i, a, b) for(int i = a; i < (b); ++i)
#define all(x) begin(x), end(x)
#define sz(x) (int)(x).size()

// typedef
typedef long long ll;
typedef unsigned int UI;
typedef unsigned long long int ULLI;
typedef unsigned short int US;
typedef pair<int,int> pii;
typedef pair<ll,ll> plli;
typedef vector<int> vi;
typedef vector<vector<int>> vvi;
typedef vector<ll> vlli;
typedef vector<pii> vpii;
typedef vector<plli> vplli;

// ---------- END OF TEMPLATE ----------

struct Dinic {
	struct Edge {
		int to, rev;
		ll c, oc;
		ll flow() { return max(oc - c, 0LL); } // if you need flows
        //Edge(int a, int b, ll c, ll rcap): to(a), rev(b), c(c), oc(rcap) {}
	};
	vector<int> lvl, ptr, q;
	vector<vector<Edge>> adj;
	Dinic(int n) : lvl(n), ptr(n), q(n), adj(n) {}
	void addEdge(int a, int b, ll c, ll rcap = 0) {
		//adj[a].emplace_back(b, int((adj[b]).size()), c, c);
		//adj[b].emplace_back(a, int((adj[a]).size()) - 1, rcap, rcap);
        adj[a].push_back({b, int((adj[b]).size()), c, c});
		adj[b].push_back({a, int((adj[a]).size()) - 1, rcap, rcap});
	}
	ll dfs(int v, int t, ll f) {
		if (v == t || !f) return f;
		for (int& i = ptr[v]; i < int((adj[v]).size()); i++) {
			Edge& e = adj[v][i];
			if (lvl[e.to] == lvl[v] + 1)
				if (ll p = dfs(e.to, t, min(f, e.c))) {
					e.c -= p, adj[e.to][e.rev].c += p;
					return p;
				}
		}
		return 0;
	}
	ll calc(int s, int t) {
		ll flow = 0; q[0] = s;
        for(int L=0; L<31; L++){ // 'int L=30' maybe faster for random data
            do {
                lvl = ptr = vector<int>(int((q).size()));
                int qi = 0, qe = lvl[s] = 1;
                while (qi < qe && !lvl[t]) {
                    int v = q[qi++];
                    for (Edge e : adj[v])
                        if (!lvl[e.to] && e.c >> (30 - L))
                            q[qe++] = e.to, lvl[e.to] = lvl[v] + 1;
                }
                while (ll p = dfs(s, t, LLONG_MAX)) flow += p;
            } while (lvl[t]);
        }
		return flow;
	}
	bool leftOfMinCut(int a) { return lvl[a] != 0; }
    map<pair<int,int>, ll> getflow() {
        map<pair<int,int>, ll> flow;
        for(int i=0; i<int((adj).size()); i++){
            for(int j=0; j<int((adj[i]).size()); j++){
                flow[{i, adj[i][j].to}] = adj[i][j].flow();
            }
        }
        return flow;
    }
};

int sing_lang[1005][10005], song_lang[1005][10005];

int main(){
    fastio;
    int n, m, k;
    cin>>n>>m>>k;
    int cur = n+m;
	Dinic dinic(n+m+2*k+4);
    vector<tuple<int,int,int>> repertoires;
    for(int i=0; i<k; i++){
        int p, s, l;
        cin>>p>>s>>l;
        p--;s--;l--;
        repertoires.eb(p, l, s);
        if(!sing_lang[p][l]){
            dinic.addEdge(p, cur, 1);
            sing_lang[p][l] = cur++;
        }
        if(!song_lang[s][l]){
            dinic.addEdge(cur, n+s, 1);
            song_lang[s][l] = cur++;
        }
        dinic.addEdge(sing_lang[p][l], song_lang[s][l], 1);
    }
    int s=cur++, t=cur++;
    for(int i=0; i<n; i++) dinic.addEdge(s, i, 1e9);
    for(int i=0; i<m; i++) dinic.addEdge(n+i, t, 1e9);
    dinic.addEdge(t, s, 1e9);
    int s1=cur++, t1=cur++;
    for(int i=0; i<n; i++) dinic.addEdge(s1, i, 1);
    for(int i=0; i<m; i++) dinic.addEdge(n+i, t1, 1);
    dinic.addEdge(s1, t, m);
    dinic.addEdge(s, t1, n);
    ll mf = dinic.calc(s1, t1);
    if(mf < n+m){
        cout << -1 << endl;
        return 0;
    }
    map<pii, ll> flow = dinic.getflow();
    vi ans;
    for(int i=0; i<k; i++){
        auto[p, l, s] = repertoires[i];
        if(flow[{p, sing_lang[p][l]}]==1 && flow[{song_lang[s][l], n+s}]==1){
            ans.pb(i+1);
        }
    }
    size_t sz = sz(ans);
    cout << sz << endl;
    for(int i=0; i<sz; i++) cout << ans[i] << " \n"[i==sz-1];
}