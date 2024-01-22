// FENWICK 0-indexed range query

const int N = 200005;
int bit[N];
int a[N];
struct Fenwick {
    void initialize(int a[]){
        for (int i = 0; i < N; i++) {
            bit[i] += a[i];
            int j = i | (i + 1);
            if (j < N) bit[j] += bit[i];
        }
    }
    int sum(int r) {
        int ret = 0;
        for (; r >= 0; r = (r & (r + 1)) - 1)
            ret += bit[r];
        return ret;
    }
    int sum(int l, int r) {
        return sum(r) - sum(l - 1);
    }
    void add(int idx, int delta) {
        for (; idx < N; idx = idx | (idx + 1))
            bit[idx] += delta;
    }
} fen;

// FENWICK range update

const int N = 1e5;
int bit[N];
struct Fenwick {
    void update(int pos, int delta) {
		for (; pos < N; pos |= pos + 1) bit[pos] += delta;
	}
    void range_add(int l, int r, int v){ // 0-indexed
        fen.update(l, v);
        fen.update(r + 1, -v);
    }
    int query(int pos) { // 1-indexed
		int res = 0;
		for (; pos > 0; pos &= pos - 1) res += bit[pos - 1];
		return res;
	}
} fen;

// FENWICK 1-indexed range update & range query

const int N = 200005;
int B1[N], B2[N];
int a[N];
struct Fenwick {
    void initialize(int a[]){
        for (int i = 1; i <= N; i++) {
            range_add(i, i, a[i - 1]);
        }
    }
    void add(int b[], int idx, int delta) {
        for (; idx <= N; idx += idx & -idx)
            b[idx] += delta;
    }
    void range_add(int l, int r, int delta){
        add(B1, l, delta);
        add(B1, r + 1, -delta);
        add(B2, l, delta * (l - 1));
        add(B2, r + 1, -delta * r);
    }
    int sum(int b[], int idx){
        int ret = 0;
        for (; idx > 0; idx -= idx & -idx)
            ret += b[idx];
        return ret;
    }
    int prefix_sum(int idx){
        return sum(B1, idx) * idx - sum(B2, idx);
    }
    int range_sum(int l, int r){
        return prefix_sum(r) - prefix_sum(l - 1);
    }
} fen;