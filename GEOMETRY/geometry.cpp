template <class T> int sgn(T x) { return (x > 0) - (x < 0); }
template<class T>
struct Point {
	typedef Point P;
	T x, y;
	explicit Point(T x=0, T y=0) : x(x), y(y) {}
	bool operator<(P p) const { return tie(x,y) < tie(p.x,p.y); }
	bool operator==(P p) const { return tie(x,y)==tie(p.x,p.y); }
	P operator+(P p) const { return P(x+p.x, y+p.y); }
	P operator-(P p) const { return P(x-p.x, y-p.y); }
	P operator*(T d) const { return P(x*d, y*d); }
	P operator/(T d) const { return P(x/d, y/d); }
	T dot(P p) const { return x*p.x + y*p.y; }
	T cross(P p) const { return x*p.y - y*p.x; }
	T cross(P a, P b) const { return (a-*this).cross(b-*this); }
	T dist2() const { return x*x + y*y; }
	double dist() const { return sqrt((double)dist2()); }
	// angle to x-axis in interval [-pi, pi]
	double angle() const { return atan2(y, x); }
	P unit() const { return *this/dist(); } // makes dist()=1
	P perp() const { return P(-y, x); } // rotates +90 degrees
	P normal() const { return perp().unit(); }
	// returns point rotated 'a' radians ccw around the origin
	P rotate(double a) const {
		return P(x*cos(a)-y*sin(a),x*sin(a)+y*cos(a)); }
	friend ostream& operator<<(ostream& os, P p) {
		return os << "(" << p.x << "," << p.y << ")"; }
};

/*
smallest surrounding rectangle

Compute the convex hull of the cloud.
For each edge of the convex hull:
compute the edge orientation (with arctan),
rotate the convex hull using this orientation in order to compute easily the bounding rectangle
area with min/max of x/y of the rotated convex hull,
Store the orientation corresponding to the minimum area found,
Return the rectangle corresponding to the minimum area found.

vector<P> hull = convexHull(p);
double ans = DBL_MAX;
for(int i=0; i<sz(hull)-1; i++){
    double a = (hull[i+1]-hull[i]).angle();
    double minx=DBL_MAX, maxx=DBL_MIN, miny=DBL_MAX, maxy=DBL_MIN;
    for(int j=0; j<sz(hull); j++){
        P w = hull[j].rotate(-a);
        minx = min(minx, w.x);
        maxx = max(maxx, w.x);
        miny = min(miny, w.y);
        maxy = max(maxy, w.y);
    }
    ans = min(ans, (maxx-minx)*(maxy-miny));
}
*/