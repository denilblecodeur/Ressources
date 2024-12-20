/*
Euclidean MST, N <= 2e5, |x|,|y| <= 1e4
https://judge.yosupo.jp/submission/220923
*/

#include <bits/stdc++.h>
using namespace std;

#define all(x) begin(x), end(x)
#ifdef CKISEKI
#include <experimental/iterator>
#define safe cerr<<__PRETTY_FUNCTION__<<" line "<<__LINE__<<" safe\n"
#define debug(a...) debug_(#a, a)
#define orange(a...) orange_(#a, a)
void debug_(auto s, auto ...a) {
  cerr << "\e[1;32m(" << s << ") = (";
  int f = 0;
  (..., (cerr << (f++ ? ", " : "") << a));
  cerr << ")\e[0m\n";
}
void orange_(auto s, auto L, auto R) {
  cerr << "\e[1;33m[ " << s << " ] = [ ";
  using namespace experimental;
  copy(L, R, make_ostream_joiner(cerr, ", "));
  cerr << " ]\e[0m\n";
}
#else
#define safe ((void)0)
#define debug(...) safe
#define orange(...) safe
#endif

namespace {

using lld = int64_t;
using P = complex<lld>;

#define RE real
#define IM imag

lld cross(P a, P b) {
  return IM(conj(a) * b);
}

int sgn(lld z) {
  return (z > 0) - (z < 0);
}
int ori(P a, P b, P c) {
  return sgn(cross(b - a, c - a));
}

using i128 = int64_t;

namespace delaunay {
const int C = 20005, maxn = 200025;

/* please ensure input points are unique */
/* A triangulation such that no points will strictly
inside circumcircle of any triangle. C should be big
enough s.t. the initial triangle contains all points */
#define L(i) ((i)==0 ? 2 : (i)-1)
#define R(i) ((i)==2 ? 0 : (i)+1)
#define F3 for (int i = 0; i < 3; i++)
bool is_inf(P z) { return RE(z) <= -C || RE(z) >= C; }
bool in_cc(const array<P,3> &p, P q) {
  i128 inf_det = 0, det = 0, inf_N, N;
  F3 {
    if (is_inf(p[i]) && is_inf(q)) continue;
    else if (is_inf(p[i])) inf_N = 1, N = -norm(q);
    else if (is_inf(q)) inf_N = -1, N = norm(p[i]);
    else inf_N = 0, N = norm(p[i]) - norm(q);
    lld D = cross(p[R(i)] - q, p[L(i)] - q);
    inf_det += inf_N * D; det += N * D;
  }
  return inf_det != 0 ? inf_det > 0 : det > 0;
}
P v[maxn];
struct Tri;
struct E {
  Tri *t; int side;
  E(Tri *t_=0, int side_=0) : t(t_), side(side_) {}
};
struct Tri {
  array<int,3> p; array<Tri*,3> ch; array<E,3> e;
  Tri(int a=0, int b=0, int c=0) : p{a, b, c}, ch{} {}
  bool has_chd() const { return ch[0] != nullptr; }
  bool contains(int q) const {
    F3 if (ori(v[p[i]], v[p[R(i)]], v[q]) < 0)
      return false;
    return true;
  }
  bool check(int q) const {
    return in_cc({v[p[0]], v[p[1]], v[p[2]]}, v[q]); }
} pool[maxn * 10], *it, *root;
/* SPLIT_HASH_HERE */
void link(const E &a, const E &b) {
  if (a.t) a.t->e[a.side] = b;
  if (b.t) b.t->e[b.side] = a;
}
void flip(Tri *A, int a) {
  auto [B, b] = A->e[a]; /* flip edge between A,B */
  if (!B || !A->check(B->p[b])) return;
  Tri *X = new (it++) Tri(A->p[R(a)], B->p[b], A->p[a]);
  Tri *Y = new (it++) Tri(B->p[R(b)], A->p[a], B->p[b]);
  link(E(X, 0), E(Y, 0));
  link(E(X, 1), A->e[L(a)]); link(E(X, 2), B->e[R(b)]);
  link(E(Y, 1), B->e[L(b)]); link(E(Y, 2), A->e[R(a)]);
  A->ch = B->ch = {X, Y, nullptr};
  flip(X, 1); flip(X, 2); flip(Y, 1); flip(Y, 2);
}
void add_point(int p) {
  Tri *r = root;
  while (r->has_chd()) for (Tri *c: r->ch)
    if (c && c->contains(p)) { r = c; break; }
  array<Tri*, 3> t; /* split into 3 triangles */
  F3 t[i] = new (it++) Tri(r->p[i], r->p[R(i)], p);
  F3 link(E(t[i], 0), E(t[R(i)], 1));
  F3 link(E(t[i], 2), r->e[L(i)]);
  r->ch = t;
  F3 flip(t[i], 2);
}
auto build(const vector<P> &p) {
  it = pool; int n = (int)p.size();
  vector<int> ord(n); iota(all(ord), 0);
  shuffle(all(ord), mt19937(114514));
  root = new (it++) Tri(n, n + 1, n + 2);
  copy_n(p.data(), n, v); v[n++] = P(-C, -C);
  v[n++] = P(C * 2, -C); v[n++] = P(-C, C * 2);
  for (int i : ord) add_point(i);
  vector<array<int, 3>> res;
  for (Tri *now = pool; now != it; now++)
    if (!now->has_chd()) res.push_back(now->p);
  return res;
}
}

struct Dsu {
  vector<int> pa, rk;
  int anc(int x) {
    return pa[x]==x ? x : pa[x] = anc(pa[x]);
  }
  bool join(int x, int y) {
    x = anc(x);
    y = anc(y);
    if (x == y) return false;
    if (rk[x] < rk[y]) swap(x, y);
    if (rk[x] == rk[y]) ++rk[x];
    pa[y] = x;
    return true;
  }
  Dsu(int n) : pa(n), rk(n) {
    iota(all(pa), 0);
  }
};

}

signed main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int N;
  cin >> N;

  vector<P> p;
  map<pair<int,int>, int> mp;
  vector<int> perm;

  vector<pair<int,int>> ans;

  for (int i = 0; i < N; i++) {
    int x, y;
    cin >> x >> y;
    if (auto it = mp.find({x, y}); it != mp.end()) {
      ans.emplace_back(it->second, i);
    } else {
      mp[{x, y}] = i;
      p.emplace_back(x, y);
      perm.emplace_back(i);
    }
  }

  orange(all(p));
  orange(all(perm));

  vector<tuple<lld, int, int>> e;
  Dsu dsu(N);

  for (auto t : delaunay::build(p)) {
    for (int j = 0; j < 3; j++) {
      int a = t[j];
      int b = t[(j + 1) % 3];
      if (a >= p.size() || b >= p.size()) continue;
      lld w = norm(p[a] - p[b]);
      e.emplace_back(w, a, b);
    }
  }

  ranges::sort(e);

  for (auto [_, a, b] : e)
    if (dsu.join(a, b))
      ans.emplace_back(perm[a], perm[b]);

  for (auto [a, b] : ans)
    cout << a << ' ' << b << '\n';


}