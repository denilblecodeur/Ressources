/*
https://judge.yosupo.jp/problem/convex_layers
While there are points remaining, remove all points on the boundary
of the convex hull of the remaining points.
For each point, determine which iteration it was removed in.
*/

typedef long double ldb;
const ldb EPS = 1e-10;
const ldb PI = atan2l(0, -1);
template <class T> int sgn(T x) { return (x > 0) - (x < 0); }
template <class T> int epssgn(T x) { return (x > EPS) - (x < -EPS); }

template<class T>
struct Point {
	typedef Point P;
	T x, y;
	explicit Point(T x = 0, T y = 0) : x(x), y(y) {}
	bool operator<(P p) const { return tie(x, y) < tie(p.x, p.y); }
	bool operator==(P p) const { return tie(x, y) == tie(p.x, p.y); }
	P operator+(P p) const { return P(x + p.x, y + p.y); }
	P operator-(P p) const { return P(x - p.x, y - p.y); }
	P operator*(T d) const { return P(x * d, y * d); }
	P operator/(T d) const { return P(x / d, y / d); }
	T dot(P p) const { return x * p.x + y * p.y; }
	T cross(P p) const { return x * p.y - y * p.x; }
	T cross(P a, P b) const { return (a - *this).cross(b - *this); }
	T dist2() const { return x * x + y * y; }
	double dist() const { return sqrt((double)dist2()); }
	// angle to x-axis in interval [-pi, pi]
	double angle() const { return atan2(y, x); }
	P unit() const { return *this / dist(); } // makes dist()=1
	P perp() const { return P(-y, x); } // rotates +90 degrees
	P normal() const { return perp().unit(); }
	// returns point rotated 'a' radians ccw around the origin
	P rotate(double a) const {
		return P(x * cos(a) - y * sin(a), x * sin(a) + y * cos(a));
	}
	friend ostream& operator<<(ostream& os, P p) {
		return os << "(" << p.x << "," << p.y << ")";
	}
};

struct dynamic_hull {
	typedef Point<ll> pll;
	struct node {
		int i, j, l, size;
		node() : i(-1), j(-1), l(-1), size(0) {}
		node(int x) : i(x), j(x), l(x), size(1) {}
	};
	int n;
	vector<pll> p;
	vector<node> t;
	dynamic_hull(vector<pll>& a) : p(a) { // needs sorted (x,y)!
		n = p.size();
		while (n != (n & -n)) n += (n & -n);
		t.resize(2 * n);
		for (int i = 0; i < a.size(); i++)
			t[i + n - 1] = node(i);
		for (int i = n - 2; i >= 0; i--) fix(i);
	}
#define lp(v) p[t[v].i]
#define rp(v) p[t[v].j]
#define nsz(v) t[v].size
	void fix(int v) {
		if (v >= n) return;
		int a = 2 * v + 1, b = a + 1;
		if (!nsz(a) || !nsz(b)) {
			if (!nsz(a)) t[v] = t[b];
			else t[v] = t[a];
			return;
		}
		ll x = p[t[b].l].x, lhs, rhs;
		t[v].l = t[a].l, t[v].size = 2;
		while (nsz(a) >= 2 || nsz(b) >= 2) {
			if (nsz(a) >= 2 && lp(a).cross(rp(a), lp(b)) >= 0)
				a = 2 * a + 1;
			else if (nsz(b) >= 2 && rp(a).cross(lp(b), rp(b)) >= 0)
				b = 2 * b + 2;
			else if (nsz(a) == 1) b = 2 * b + 1;
			else if (nsz(b) == 1) a = 2 * a + 2;
			else { // a could be vertical but not b (cross < 0)
				pll ad = rp(a) - lp(a), bd = rp(b) - lp(b);
				lhs = bd.x * (ad.x * lp(a).y + ad.y * (x - lp(a).x));
				rhs = ad.x * (bd.x * lp(b).y + bd.y * (x - lp(b).x));
				if (ad.x == 0 || lhs > rhs) // left win
					a = 2 * a + 2;
				else b = 2 * b + 1;
			}
			if (nsz(a) == 0) a = ((a - 1) ^ 1) + 1;
			if (nsz(b) == 0) b = ((b - 1) ^ 1) + 1;
		}
		t[v].i = t[a].i, t[v].j = t[b].j;
	}
	void update(int i, bool state) {
		i += n - 1;
		if (t[i].size == state) return; // correct state
		t[i] = state ? node(i - n + 1) : node();
		while (i) i = (i - 1) / 2, fix(i);
	}
	int maximize(ll a, ll b) { // point maximizing ax + by
		if (a < 0 && b == 0) return t[0].l;
		int v = 0, at = -1;
		ll mx = -inf, lopt, ropt;
		pll dir(a, b);
		while (t[v].size >= 2) {
			lopt = dir.dot(lp(v)), ropt = dir.dot(rp(v));
			if (lopt > ropt) {
				if (mx < lopt) mx = lopt, at = t[v].i;
				v = 2 * v + 1;
			}
			else {
				if (mx < ropt) mx = ropt, at = t[v].j;
				v = 2 * v + 2;
			}
			if (nsz(v) == 0) v = ((v - 1) ^ 1) + 1;
		}
		if (t[v].size == 1 && mx < dir.dot(lp(v)))
			at = t[v].i;
		return at;
	}
	void hull(vector<int> &res) {
		res.clear();
		int l = maximize(-1, 0), r = maximize(1, 0);
		if (l == -1) return;
		if (l == r) res.push_back(l);
		else hull(l, r, res), res.push_back(r);
	}
	void hull(int i, int j, vector<int>& res) {
		int k = maximize(p[i].y - p[j].y, p[j].x - p[i].x);
		if (k == i || k == j) res.push_back(i);
		else hull(i, k, res), hull(k, j, res);
	}
};

vector<int> convex_hull_layers(vector<Point<ll>> a) {
	int n = a.size();
	vector<int> orig(n);
	for (int i = 0; i < n; i++) orig[i] = i;
	sort(orig.begin(), orig.end(), [&a](int i, int j) {
		return a[i] < a[j];
		});
	sort(a.begin(), a.end());
	dynamic_hull upper(a);
	auto b = a;
	reverse(b.begin(), b.end());
	for (auto& i : b)
		i = Point<ll>(-i.x, -i.y);
	dynamic_hull lower(b);

	vector<int> ans(n);
	int iter = 1;
	while (1) {
		vector<int> up, low;
		upper.hull(up), lower.hull(low);
		if (up.size() == 0) break;
		// extend up
		int upsize = up.size();
		for (auto& i : up) upper.update(i, 0);
		for (int i = 0; i + 1 < upsize; i++) {
			Point<ll> dot = (a[up[i + 1]] - a[up[i]]).perp();
			while (1) {
				int j = upper.maximize(dot.x, dot.y);
				if (j == -1 || dot.dot(a[j]) < dot.dot(a[up[i]])) break;
				up.push_back(j);
				upper.update(j, 0);
			}
		}
		// extend low
		int lowsize = low.size();
		for (auto& i : low) lower.update(i, 0);
		for (int i = 0; i + 1 < lowsize; i++) {
			Point<ll> dot = (b[low[i + 1]] - b[low[i]]).perp(); // notice different order
			while (1) {
				int j = lower.maximize(dot.x, dot.y);
				if (j == -1 || dot.dot(b[j]) < dot.dot(b[low[i]])) break;
				low.push_back(j);
				lower.update(j, 0);
			}
		}
		// update answer and hulls
		for (auto& i : up) {
			ans[orig[i]] = iter;
			upper.update(i, 0);
			lower.update(n - 1 - i, 0);
		}
		for (auto& i : low) {
			ans[orig[n - 1 - i]] = iter;
			upper.update(n - 1 - i, 0);
			lower.update(i, 0);
		}
		iter++;
	}
	return ans;
}

void solve() {
	int n;
	cin >> n;
	vector<Point<ll>> a(n);
	for (int i = 0, x, y; i < n; i++) {
		cin >> x >> y;
		a[i] = Point<ll>(x, y);
	}
	auto ans = convex_hull_layers(a);
	for (auto& i : ans) cout << i << '\n';
}