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

struct Edge {
    int next;
    long long capacity;
    Edge(const int n, const long long c) : next(n), capacity(c) {}
};
class Dinic {
private:
    const int n;
    vector<int> idx;
    vector<int> dist;
public:
    vector<vector<int>> adj;
    vector<Edge> edges;
    Dinic(const int n):n(n),idx(n),dist(n),adj(n){}
    void add_arc(const int u, const int v, const long long capacity) {
        if (u != v && capacity != 0) {
            const int uv = edges.size();
            edges.emplace_back(v, capacity);
            const int vu = edges.size();
            edges.emplace_back(u, 0);
            adj[u].push_back(uv);
            adj[v].push_back(vu);
        }
    }
    void add_edge(const int u, const int v, const long long capacity) {
        if (u != v && capacity != 0) {
            const int uv = edges.size();
            edges.emplace_back(v, capacity);
            const int vu = edges.size();
            edges.emplace_back(u, capacity);
            adj[u].push_back(uv);
            adj[v].push_back(vu);
        }
    }
    long long dfs(const int u, const int t, const long long delta) {
        if (delta == 0)
            return 0;
        if (u == t)
            return delta;
        int& i = idx[u];
        while (i >= 0) {
            const int uv = adj[u][i];
            const int v = edges[uv].next;
            if (dist[v] == dist[u]+1) {
                const long long bottleneck = dfs(v, t, min(delta, edges[uv].capacity));
                if (bottleneck > 0) {
                    const int vu = uv ^ 1;
                    edges[uv].capacity -= bottleneck;
                    edges[vu].capacity += bottleneck;
                    return bottleneck;
                }
            }
            --i;
        };
        return 0;
    }
    long long solve(const int s, const int t) {
        long long total_flow = 0;
        for (;;) {
            // Run a BFS
            queue<int> q;
            for (int v = 0; v < n; ++v)
                dist[v] = -1;
            dist[s] = 10;
            q.push(s);
            while (!q.empty()) {
                const int u = q.front();
                q.pop();
                for (const int i : adj[u]) {
                    const Edge& uv = edges[i];
                    const int v = uv.next;
                    if (uv.capacity > 0 && dist[v] == -1) {
                        dist[v] = dist[u] + 1;
                        q.push(v);
                    }
                }
            }
            if (dist[t] == -1) break;
            for (int v = 0; v < n; ++v)
                idx[v] = adj[v].size()-1;
            for (;;) {
                const long long flow = dfs(s, t, numeric_limits<long long>::max());
                if (flow == 0) break;
                total_flow += flow;
            }
        }
        return total_flow;
    }
};
////////////////////////////////////////// BEGIN OF L-R FLOWS WITH DINIC //////////////////////////////////////////
///////////////// Note: 0-indexed vertices /////////////////
///////////////// Warning: adding an edge with demand>capacity causes runtime error /////////////////
///////////////// Note: be careful with the return value -- if the total demand is 0 and compute() returns 0, there is nonetheless a feasible flow (namely, the empty flow) /////////////////
class LRDinic {
protected:
    int n;
    vector<long long> from_source, to_sink, outgoing_capacity;
    long long total_demand;
public:
    Dinic dinic;
    LRDinic(const int n): n(n),from_source(n),to_sink(n),outgoing_capacity(n),total_demand(0),dinic(n+2){}
    void add_arc(const int u, const int v, const long long demand, const long long capacity) {
        assert(capacity >= demand);
        if (u != v) {
            from_source[v] += demand;
            to_sink[u] += demand;
            dinic.add_arc(u, v, capacity-demand);
            total_demand += demand;
            outgoing_capacity[u] += capacity;
        }
    }
    long long compute(const int s, const int t) {
        // Add extra edges
        const int source = n;
        const int sink = n+1;
        int extra_edges = 0;
        for (int v = 0; v < n; ++v) {
            if (from_source[v] != 0) {
                ++extra_edges;
                dinic.add_arc(source, v, from_source[v]);
            }
            if (to_sink[v] != 0) {
                ++extra_edges;
                dinic.add_arc(v, sink, to_sink[v]);
            }
        }
        dinic.add_arc(t, s, std::numeric_limits<long long>::max());
        ++extra_edges;
        // Compute a feasible flow in G (by computing a saturating flow in G')
        long long flow_aux = dinic.solve(source, sink);
        if (flow_aux != total_demand)
            return 0;
        // Remove extra edges
        while (extra_edges--) {
            dinic.adj[dinic.edges.back().next].pop_back();
            dinic.edges.pop_back();
            dinic.adj[dinic.edges.back().next].pop_back();
            dinic.edges.pop_back();
        }
        // Extend the current flow to a maximum flow
        dinic.solve(s, t);
        long long flow = outgoing_capacity[s];
        for (const int idx : dinic.adj[s])
            flow -= dinic.edges[idx].capacity;
        return flow;
    }
};
class LRDinicRetrieval : public LRDinic {
private:
    vector<map<int, long long>> original_capacity;
public:
    LRDinicRetrieval(const int n):LRDinic(n),original_capacity(n){}
    void add_arc(const int u, const int v, const long long demand, const long long capacity) {
        LRDinic::add_arc(u, v, demand, capacity);
        original_capacity[u][v] += capacity;
        original_capacity[v][u] -= capacity;
    }
    vector<map<int, long long>> retrieve_skew_flow() {
        vector<map<int, long long>> ans = original_capacity;
        for (int u = 0; u < n; ++u) {
            for (const int idx : dinic.adj[u]) {
                if ((idx&1) == 0) {
                    const Edge& e = dinic.edges[idx];
                    const int v = e.next;
                    ans[u][v] -= e.capacity;
                    ans[v][u] += e.capacity;
                }
            }
        }
        for (int u = 0; u < n; ++u) {
            for (auto it = ans[u].begin(), end=ans[u].end(); it != end; )
                if (it->second == 0)
                    it = ans[u].erase(it);
                else
                    ++it;
        }
        return ans;
    }
    vector<map<int, long long>> retrieve_gross_flow() {
        // Note: returns skew-symmetric flow
        vector<map<int, long long>> ans = original_capacity;
        for (int u = 0; u < n; ++u) {
            for (const int idx : dinic.adj[u]) {
                if ((idx&1) == 0) {
                    const Edge& e = dinic.edges[idx];
                    const int v = e.next;
                    ans[u][v] -= e.capacity;
                    ans[v][u] += e.capacity;
                }
            }
        }
        for (int u = 0; u < n; ++u) {
            for (auto it = ans[u].begin(), end=ans[u].end(); it != end; )
                if (it->second <= 0) it = ans[u].erase(it);
                else ++it;
        }
        return ans;
    }
};

int sing_lang[1005][10005], song_lang[1005][10005];

int main(){
    fastio;
    int n, m, k;
    cin >> n >> m >> k;
    int source=0, target=n+2*k+m+1;
	LRDinicRetrieval dinic(target+1);
    vector<tuple<int,int,int>> repertoires;
    for(int i=0; i<k; i++){
        int p, s, l;
        cin >> p >> s >> l;
        repertoires.eb(p, l, s);
        if(!sing_lang[p][l]){
            sing_lang[p][l] = 1;
            dinic.add_arc(p, n+l, 0, 1);
        }
        if(!song_lang[s][l]){
            song_lang[s][l] = 1;
            dinic.add_arc(n+k+l, n+2*k+s, 0, 1);
        }
        dinic.add_arc(n+i+1, n+k+i+1, 0, 1);
    }
    for(int i=0; i<n; i++){
        dinic.add_arc(source, i+1, 1, 1e9);
    }
    for(int i=0; i<m; i++){
        dinic.add_arc(n+2*k+i+1, target, 1, 1e9);
    }
    ll mf = dinic.compute(source, target);
    cout << mf << endl;
    if(mf < n+m){
        cout << -1 << endl;
        return 0;
    }
    auto flow = dinic.retrieve_gross_flow();
    vi ans;
    for(int i=0; i<k; i++){
        auto[p, l, s] = repertoires[i];
        if(flow[p][n+l] && flow[n+l][n+k+l] && flow[n+k+l][n+2*k+s]){
            ans.pb(i+1);
        }
    }
    size_t sz = sz(ans);
    cout << sz << endl;
    for(int i=0; i<sz; i++) cout << ans[i] << " \n"[i==sz-1];
}