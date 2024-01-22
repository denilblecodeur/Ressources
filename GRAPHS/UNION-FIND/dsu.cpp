struct DSU {
   vector<int> up;
   DSU(int N) { up = vector<int>(N, -1); }
   int get(int x) { return up[x] < 0 ? x : up[x] = get(up[x]); }
   bool same_set(int a, int b) { return get(a) == get(b); }
   int size(int x) { return -up[get(x)]; }
   bool unite(int x, int y) {
      x = get(x), y = get(y);
      if (x == y) return false;
      if (up[x] > up[y]) swap(x, y);
      up[x] += up[y];
      up[y] = x;
      return true;
   }
};

// faster
class union_find {
    vector<int> tree;
    public:
    union_find(int n): tree(n, -1) { }
    int root(int i){
        if(tree[i]<0) return i;
        return tree[i] = root(tree[i]);
    };
    bool unite(int i, int j){
        int ri = root(i);
        int rj = root(j);
        if(ri == rj) return false;
        if(tree[ri] > tree[rj]) swap(ri, rj);
        tree[ri] += tree[rj];
        tree[rj] = ri;
        return true;
    }
};