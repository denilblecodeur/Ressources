template <class T> class MergeSortTree {
public:
    int _l, _r, _m;
    vector<T> v;
    MergeSortTree *left, *right;
    MergeSortTree(int l, int r, vector<T> &e) {
        _l = l, _r = r, _m = (l + r) / 2;
        v.resize(r - l + 1);
        if (l == r) {
            v[0] = e[l];
            left = right = nullptr;
        } else {
            left = new MergeSortTree(_l, _m, e);
            right = new MergeSortTree(_m + 1, _r, e);
            merge(left->v.begin(), left->v.end(), right->v.begin(), right->v.end(), v.begin());
        }
    }
    int count(int l, int r, T a, T b) { // Nombre de x -> a<=x<=b et x est entre l et r
        if (l > _r || r < _l) return 0;
        if (_l >= l && _r <= r) {
            return upper_bound(v.begin(), v.end(), b) - lower_bound(v.begin(), v.end(), a);
        }
        return left->count(l, r, a, b) + right->count(l, r, a, b);
    }
};