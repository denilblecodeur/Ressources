#include <bits/stdc++.h>
using namespace std; 
 
struct DSU {
    vector<int> f;
    DSU(int n) : f(n + 1, -1) {};
    int find(int x) {
        return f[x] < 0 ? x : f[x] = find(f[x]);
    }
    bool merge(int x, int y) {
        x = find(x);
        y = find(y);
        if (x == y) return false;
        if (f[x] > f[y]) swap(x, y);
        f[x] += f[y];
        f[y] = x;
        return true;
    }
    int siz(int x) {
        return -f[find(x)];
    }
};
 
constexpr int inf = 21e8;
 
struct Min {
    pair<int, int> x;
    Min(pair<int, int> x = {inf, -1}) : x(move(x)) {}
    Min operator+=(const Min &ano) {
        x = min(x, ano.x);
        return *this;
    }
    bool operator==(const Min &ano) const {
        return x == ano.x;
    }
    friend Min operator+(const Min &lhs, const Min &rhs) {
        Min ret = lhs;
        ret += rhs;
        return ret;
    }
};
 
template<typename T>
struct Fenwick {
    int n;
    vector<T> t;
    Fenwick(int _n) : n(_n + 1), t(_n + 2) {};
    void update(int x, T v) {
        x++;
        for (; x <= n; x += x & -x) {
            t[x] = t[x] + v;
        }
    }
    T query(int x) {
        x++;
        T ret{};
        for (; x; x -= x & -x) {
            ret = ret + t[x];
        }
        return ret;
    }
    T query(int l, int r) {
        return query(r) - query(l - 1);
    }
};
 
 
auto manhattan_mst(vector<pair<int, int>> ps) {
    int n = ps.size();
    vector<array<int, 3>> es;
    for (int j = 0; j < 4; ++j) {
        for (auto &[x, y]: ps) {
            if (j & 1) {
                swap(x, y);
            }
            if (j == 2) {
                x = -x;
            }
        }
        vector<int> ord(n);
        iota(ord.begin(), ord.end(), 0);
        sort(ord.begin(), ord.end(), [&](int i, int j) {
            return ps[i] > ps[j];
        });
        vector<int> val(n);
        for (int i = 0; i < n; ++i) {
            auto [x, y] = ps[i];
            val[i] = x - y;
        }
        auto vec = val;
        sort(vec.begin(), vec.end());
        vec.erase(unique(vec.begin(), vec.end()), vec.end());
        auto get = [&](int v) {
            return (int) (lower_bound(vec.begin(), vec.end(), v) - vec.begin());
        };
        // Min initial: {inf, -1}
        Fenwick<Min> t((int) vec.size());
        for (int i = 0; i < n; ++i) {
            int u = ord[i];
            int id = get(val[u]);
            auto [x, y] = ps[u];
            auto [_, v] = t.query(id).x;
            if (v != -1) {
                auto [x1, y1] = ps[v];
                int d = abs(x - x1) + abs(y - y1);
                es.push_back({d, u, v});
            }
            t.update(id, make_pair(x + y, u));
        }
    }
    sort(es.begin(), es.end());
    return es;
}
 
void solve() {
    int X, Y, n;
    cin >> X >> Y >> n;
    vector<pair<int, int>> ps(n);
 
    int s = -1, t = -1;
    for (int i = 0; i < n; ++i) {
        auto &[x, y] = ps[i];
        cin >> x >> y;
        if (x == 1 && y == 1) s = i;
        if (x == X && y == Y) t = i;
    }
 
    auto es = manhattan_mst(ps);
 
    DSU dsu(n);
    int ans = 0;
    for (auto [w, u, v]: es) {
        if (dsu.find(s) == dsu.find(t)) break;
        dsu.merge(u, v);
        ans = w / 2;
    }
    cout << ans << '\n';
}
 
int main() {
    ios_base::sync_with_stdio(false); cin.tie(nullptr);
    int t; cin >> t;
    while(t--){
        solve();
    }
}