
#include <bits/stdc++.h>

using namespace std;

#define forn(i, n) for (int i = 0; i < (int)(n); i++)
#define all(a) (a).begin(), (a).end()

typedef int tResult;
tResult Zero = 0;
inline tResult recalc( tResult a, tResult b ) { return a + b; }

template <class T, const bool (*cmp)(T*, T*), const bool (*cmpi)(T*, T*), class DataStructure>
struct SegmentTree {
  DataStructure *d;
  vector<T*> a;
  int n;

  SegmentTree() {
    a.clear();
  }
  void add( T *item ) {        
    a.push_back(item);
  }
  void build() {
    n = a.size();
    sort(all(a), cmpi);
    d = new DataStructure[2 * n];
    forn(i, n)
      for (int j = i + n; j > 0; j >>= 1)
        d[j].add(a[i]);
    forn(i, 2 * n)
      d[i].build();
  }
  tResult get( T *L, T *R ) {
    int l = lower_bound(all(a), L, cmp) - a.begin();
    int r = upper_bound(all(a), R, cmp) - a.begin() - 1;
    tResult res = Zero;
    for (l += n, r += n; l <= r; l >>= 1, r >>= 1) {
      if (l % 2 == 1) res = recalc(res, d[l++].get(L, R));
      if (r % 2 == 0) res = recalc(res, d[r--].get(L, R));
    }
    return res;
  }
  void change( T *item ) {
    int i = lower_bound(all(a), item, cmpi) - a.begin();
    for (int j = i + n; j > 0; j >>= 1)
      d[j].change(item);
  }
};

template <class T, const bool (*cmp)(T*, T*), const bool (*cmpi)(T*, T*)>
struct SegmentTree1D {
  tResult *f;
  vector<T*> a;
  int n;

  SegmentTree1D() {
    a.clear();
  }
  void add( T *item ) { 
    a.push_back(item);
  }
  void calc( int i ) {
    f[i] = recalc(f[2 * i], f[2 * i + 1]);
  }
  void build() {
    n = a.size();
    f = new tResult[2 * n];
    sort(all(a), cmpi);
    forn(i, n)
      f[i + n] = a[i]->get();
    for (int i = n - 1; i > 0; i--)
      calc(i);
  }
  tResult get( T *L, T *R ) {
    int l = lower_bound(all(a), L, cmp) - a.begin();
    int r = upper_bound(all(a), R, cmp) - a.begin() - 1;
    tResult res = Zero;
    for (l += n, r += n; l <= r; l >>= 1, r >>= 1) {
      if (l % 2 == 1) res = recalc(res, f[l++]);
      if (r % 2 == 0) res = recalc(res, f[r--]);
    }
    return res;
  }
  void change( T *item ) {
    int i = lower_bound(all(a), item, cmpi) - a.begin();
    f[i += n] = item->get();
    for (i >>= 1; i > 0; i >>= 1)
      calc(i);
  }
};

template <class T, const bool (*cmp)(T*, T*)>
struct SortedArray {
  vector<T*> a;
  SortedArray() {
    a.clear();
  }
  void add( T *item ) { 
    a.push_back(item);
  }
  void build() {
    sort(all(a), cmp);
  }
  tResult get( T *L, T *R ) {
    tResult f = Zero;
    for (auto r = upper_bound(all(a), R, cmp), l = lower_bound(all(a), L, cmp); l < r; l++)
      f = recalc(f, (*l)->get());
    return f;
  }
  void change( T *item ) { }
};

struct pnt2d {
  int x, y, value;
  tResult get() { return value; }
};

#define LESS(T, X) \
  static const bool T##_##X(T *a, T *b) { return a->X < b->X; } \
  static const bool T##_##X##i(T *a, T *b) { return make_pair(a->X, a) < make_pair(b->X, b); }
LESS(pnt2d, x)
LESS(pnt2d, y)

#define STree(T, X, D) SegmentTree<T, T##_##X, pnt2d##_##X##i, D>
#define STree1D(T, X) SegmentTree1D<T, T##_##X, pnt2d##_##X##i>

typedef SortedArray<pnt2d, pnt2d_y> SortedArrayY;
typedef STree1D(pnt2d, y) STreeY;
STree(pnt2d, x, SortedArrayY) ds_slow;
STree(pnt2d, x, STreeY) ds;
