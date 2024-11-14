/**
 * Implicit Treap
 * 0-indexed
 * Example of use:
		IT treap;
		treap.insert(position, value);
		treap.query<int>(l, r+1, f());
		treap.upd(l, r+1, f());
		treap.get_vector();
		for(auto x : treap.result_vector)
 */

mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

typedef struct item * pitem;
struct item {
    int prior, val, sum=0, add=0, size=1;
	bool rev=false;
    pitem l=nullptr, r=nullptr;
    item(int val) : val(val), prior(rng()) {}
};

int size(pitem p) { return p ? p->size : 0; }
int sum(pitem p) { return p ? p->sum : 0; }

void push(pitem t) {
	if (!t) { return; }
	if (t->add) {
		t->val += t->add;
        t->sum += t->size * t->add;
		if (t->l) { t->l->add += t->add; }
		if (t->r) { t->r->add += t->add; }
		t->add = 0;
	}
	if (t->rev) {
        t->rev = false;
        swap (t->l, t->r);
        if (t->l) t->l->rev ^= true;
        if (t->r) t->r->rev ^= true;
    }
}

void pull(pitem t) {
    if (!t) { return; }
    push(t->l), push(t->r);
    t->size = size(t->l) + size(t->r) + 1;
    t->sum = t->val + sum(t->l) + sum(t->r);
}

void merge(pitem &t, pitem l, pitem r) {
    push(l), push(r);
	if (!l || !r) {
		t = l ? l : r;
	} else if (l->prior > r->prior) {
		merge(l->r, l->r, r), t = l;
	} else {
		merge(r->l, l, r->l), t = r;
	}
	pull(t);
}

// splits treap into l, r; l: [0, val), r: [val, )
void split(pitem t, pitem &l, pitem &r, int val) {
	if (!t) return void(l = r = nullptr);
    push(t);
	if (val > size(t->l)) {
		split(t->r, t->r, r, val - size(t->l) - 1), l = t;
	} else {
		split(t->l, l, t->l, val), r = t;
	}
	pull(t);
}

function<void(pitem)> range_add(int v) {
	return [v](pitem t) { t->add += v; };
}
function<void(pitem)> reverse() {
	return [](pitem t) { t->rev ^= true; };
}
function<int(pitem)> range_sum() {
	// int return value
	return [](pitem t) { return t->sum; };
}

struct IT {
	pitem root = nullptr;
    vector<int> result_vector;

	void insert(int i, int x) {
        pitem l, r;
        split(root, l, r, i);
        merge(l, l, new item(x));
        merge(root, l, r);
	}

	void del(int i) {
		pitem l, r;
		split(root, l, r, i);
		split(r, root, r, 1);
		merge(root, l, r);
	}

    /**
	 * updates the range [l, r)
	 * @param f the function to apply to the range
	 */
	void upd(int l, int r, function<void(pitem)> f) {
		pitem a, b, c;  // a: [0, l); b: [l, r); c: [r, )
		split(root, a, b, l);
		split(b, b, c, r - l);
		if (b) { f(b); }
		// merge all the splits back into the main t
		merge(root, a, b);
		merge(root, root, c);
	}

    /**
	 * queries the range [l, r)
	 * @param f a query function (see use below)
	 */
	template <typename R> R query(int l, int r, function<R(pitem)> f) {
		pitem a, b, c;  // a: [0, l); b: [l, r); c: [r, )
		split(root, a, b, l);
		split(b, b, c, r - l);
		assert(b);
		R x = f(b);
		merge(root, a, b);
		merge(root, root, c);
		return x;
	}

    void each(pitem t, const function<void(pitem)> &f) {
        if(!t) return;
        push(t);
        each(t->l, f);
        f(t);
        each(t->r, f);
    }

    void get_vector() {
        each(root, [this](pitem x) { result_vector.push_back(x->val); });
    }

    void output() {
        each(root, [](pitem x) { printf("(%d, %d) ", x->val, x->sum); });
    }
};