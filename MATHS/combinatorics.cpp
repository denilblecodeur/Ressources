struct mint {
	const static int M = 998244353;
	ll v = 0;
	mint() {}
	mint(ll v) { this->v = (v % M + M) % M; }
	mint operator+(const mint &o) const { return v + o.v; }
	mint &operator+=(const mint &o) {
		v = (v + o.v) % M;
		return *this;
	}
	mint operator*(const mint &o) const { return v * o.v; }
	mint operator-(const mint &o) const { return v - o.v; }
	mint &operator-=(const mint &o) {
		mint t = v - o.v;
		v = t.v;
		return *this;
	}
	mint operator^(int y) const {
		mint r = 1, x = v;
		for (y <<= 1; y >>= 1; x = x * x)
			if (y & 1) r = r * x;
		return r;
	}
	mint inv() const {
		assert(v);
		return *this ^ M - 2;
	}
	friend istream &operator>>(istream &s, mint &v) {
		return s >> v.v;
		return s;
	}
	friend ostream &operator<<(ostream &s, const mint &v) { return s << v.v; }
	mint operator/(mint o) { return *this * o.inv(); }
};
namespace combinatorics {
    std::vector<mint> fact_, ifact_, inv_;
 
    void reserve(int size) {
        fact_.reserve(size + 1);
        ifact_.reserve(size + 1);
        inv_.reserve(size + 1);
    }
 
    void resize(int size) {
        if (fact_.empty()) {
            fact_ = {mint(1), mint(1)};
            ifact_ = {mint(1), mint(1)};
            inv_ = {mint(0), mint(1)};
        }
        for (int pos = fact_.size(); pos <= size; pos++) {
            fact_.push_back(fact_.back() * mint(pos));
            inv_.push_back(-inv_[MOD % pos] * mint(MOD / pos));
            ifact_.push_back(ifact_.back() * inv_[pos]);
        }
    }
 
    struct combinatorics_info {
        std::vector<mint> &data;
 
        combinatorics_info(std::vector<mint> &data) : data(data) {}
 
        mint operator[](int pos) {
            if (pos >= int(data.size()))
                resize(pos);
 
            return data[pos];
        }
    } fact(fact_), ifact(ifact_), inv(inv_);
 
    mint choose(int n, int k) {
        if (n < k || k < 0 || n < 0)
            return mint(0);
 
        return fact[n] * ifact[k] * ifact[n - k];
    }
}
 
using combinatorics::fact;
using combinatorics::ifact;
using combinatorics::inv;
using combinatorics::choose;
 
namespace ext_combinatorics {
    // distribute n equal elements into k groups
    mint distribute(int n, int k) {
        return choose(n + k - 1, n);
    }
 
    // count number of seqs with n '(' and m ')' and bal always >= 0
    mint catalan_nm(int n, int m) {
        assert(n >= m);
        return choose(m + n, m) - choose(m + n, m - 1);
    }
 
    mint catalan(int n) {
        return catalan_nm(n, n);
    }
 
    // count number of bracket seqs, bal always >= 0
    mint catalan_bal(int n, int start_balance = 0, int end_balance = 0) {
        if ((n + start_balance + end_balance) % 2 != 0) return 0;
        if (start_balance < 0 || end_balance < 0) return 0;
        return choose(n, (n + end_balance - start_balance) / 2) - choose(n, (n - end_balance - start_balance - 2) / 2);
    }
 
    // from (0, 0) to (x, y)
    mint grid_path(int x, int y) {
        return choose(x + y, x);
    }
 
    // from (0, 0) to (x, y) not touch low y=x+b
    mint grid_path_low(int x, int y, int b) {
        if (b >= 0) return 0;
        return grid_path(x, y) - grid_path(y - b, x + b);
    }
 
    // from (0, 0) to (x, y) not touch up y=x+b
    // O((x + y) / |b2 - b1|)
    mint grid_path_up(int x, int y, int b) {
        if (b <= 0) return 0;
        return grid_path(x, y) - grid_path(y - b, x + b);
    }
 
    // from (0, 0) to (x, y) touch L -LU +LUL -LULU ....
    // O((x + y) / |b2 - b1|)
    mint grid_calc_LUL(int x, int y, int b1, int b2) {
        swap(x, y);
        x -= b1;
        y += b1;
        if (x < 0 || y < 0) return 0;
        return grid_path(x, y) - grid_calc_LUL(y, x, -b2, -b1);
    }
 
    // from (0, 0) to (x, y) not touch low y=x+b1, up y=x+b2
    // O((x + y) / |b2 - b1|)
    mint grid_path_2(int x, int y, int b1, int b2) {
        return grid_path(x, y) - grid_calc_LUL(x, y, b1, b2) - grid_calc_LUL(y, x, -b2, -b1);
    }
 
    // probability what we end in L+R after infinity random walk, if we start at L, and absorbing points is 0, L+R.
    mint gambler_ruin_right(int L, int R, mint p_right) {
        assert(L >= 1 && R >= 1);
        if (p_right * 2 == 1) return mint(L) / mint(L + R);
        if (p_right == 1) return 1;
        if (p_right == 0) return 0;
        mint v = (1 - p_right) / p_right;
        return (1 - v.power(L)) / (1 - v.power(L + R));
    }
 
    mint gambler_ruin_left(int L, int R, mint p_left) {
        return 1 - gambler_ruin_right(L, R, 1 - p_left);
    }
}
using ext_combinatorics::catalan_bal;