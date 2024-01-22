/*
takes a bipartite graph as input
and produces a maximum-cardinality matching
time complexity O(E√V)
*/
#include <bits/stdc++.h>
using namespace std;

using PII = pair<int, int>;

struct HopcroftKarp {
  vector<int> g, l, r;
  int ans;
  HopcroftKarp(int n, int m, const vector<PII> &e)
      : g(e.size()), l(n, -1), r(m, -1), ans(0) {
    vector<int> deg(n + 1);
    for (int i=0; i<(int)e.size(); i++) deg[e[i].first]++;
    for (int i = 1; i <= n; i++) deg[i] += deg[i - 1];
    for (int i=0; i<(int)e.size(); i++) g[--deg[e[i].first]] = e[i].second;

    vector<int> a, p, q(n);
    for (;;) {
      a.assign(n, -1), p.assign(n, -1);
      int t = 0;
      for (int i = 0; i < n; i++)
        if (l[i] == -1) q[t++] = a[i] = p[i] = i;

      bool match = false;
      for (int i = 0; i < t; i++) {
        int x = q[i];
        if (~l[a[x]]) continue;
        for (int j = deg[x]; j < deg[x + 1]; j++) {
          int y = g[j];
          if (r[y] == -1) {
            while (~y) r[y] = x, swap(l[x], y), x = p[x];
            match = true, ans++;
            break;
          }

          if (p[r[y]] == -1)
            q[t++] = y = r[y], p[y] = x, a[y] = a[x];
        }
      }

      if (!match) break;
    }
  }
};

void solve() {
  int l, r;
  cin >> l;
  vector<PII> tv(l);
  for(int i=0; i<l; i++){
    int h, l; cin >> h >> l;
    tv[i] = make_pair(h, l);
  }
  cin >> r;
  vector<PII> buyer(r);
  for(int i=0; i<r; i++){
    int h, l; cin >> h >> l;
    buyer[i] = make_pair(h, l);
  }

  vector<PII> e;
  for(int i=0; i<l; i++){
    for(int j=0; j<r; j++){
        if(tv[i].first >= buyer[j].first && tv[i].second >= buyer[j].second){
            e.push_back(make_pair(i, j));
        }
    }
  }
  HopcroftKarp hk(l, r, e);
  cout << hk.ans << "\n";
  for (int i = 0; i < l; i++) {
    if (~hk.l[i]) {
      cout << i << " " << hk.l[i] << "\n";
    }
  }
}

int main() {
  solve();
  return 0;
}