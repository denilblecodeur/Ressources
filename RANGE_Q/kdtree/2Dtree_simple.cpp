
#include <bits/stdc++.h>

using namespace std;

#define all(a) (a).begin(), (a).end()

/**
  n, p[]
  precalc : nlogn
  get     : log^2(n), #{i : L <= i <= R, x <= p[i] <= y}
*/

struct Tree2D {
  int n;
  vector<int> *t;

  void build( int _n, int *p ) {
    n = _n;
    t = new vector<int>[2 * n];
    for (int i = n - 1; i > 0; i--) {
      t[i].resize(t[2 * i].size() + t[2 * i + 1].size());
      merge(all(t[2 * i]), all(t[2 * i + 1]), t[i].begin());
    }
  }

  inline int inner_get( int i, int x, int y ) {
    return upper_bound(all(t[i]), y) - lower_bound(all(t[i]), x);
  }

  int get( int l, int r, int x, int y ) { // 0 <= l <= r < n, [l..r] * [x..y]
    int cnt = 0;
    for (l += n, r += n; l <= r; l >>= 1, r >>= 1) {
      if ((l & 1) == 1) cnt += inner_get(l++, x, y);
      if ((r & 1) == 0) cnt += inner_get(r--, x, y);
    }
    return cnt;
  }
};
