
#include <cstdio>
#include <cmath>
#include <algorithm>

using namespace std;

/**
  n, p[]
  precalc : nlogn
  get     : log^2(n), #{i : L <= i <= R, x <= p[i] <= y}
*/

struct Tree2D {
  int n, *mem, **t;

  void alloc( int _n ) {
    n = _n, mem = new int[(int)ceil(n * (log(n) / log(2.0) + 1) + 1e-9)];
  }

  void build( int *p ) {
    int *cur = mem;
    t = new int* [2 * n];
    for (int i = n; i < 2 * n; i++)
      t[i] = cur++, t[i][0] = p[i - n];
    for (int s = 1, l = (n + 1) / 2, r = (2 * n - 2) / 2; l <= r; l = (l + 1) / 2, r = (r - 1) / 2, s *= 2)
      for (int i = l; i <= r; i++)
        merge(t[2 * i], t[2 * i] + s, t[2 * i + 1], t[2 * i + 1] + s, t[i] = cur), cur += s * 2;
  }

  inline int inner_get( int i, int s, int x, int y ) {
    return upper_bound(t[i], t[i] + s, y) - lower_bound(t[i], t[i] + s, x);
  }

  int get( int l, int r, int x, int y ) { // 0 <= l <= r < n, [l..r] * [x..y]
    int cnt = 0, s;
    if (x > y)
      return 0;
    for (l += n, r += n, s = 1; l <= r; l >>= 1, r >>= 1, s <<= 1) {
      if ((l & 1) == 1) cnt += inner_get(l++, s, x, y);
      if ((r & 1) == 0) cnt += inner_get(r--, s, x, y);
    }
    return cnt;
  }
};
