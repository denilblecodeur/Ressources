void init_sparse(vector<int>&a, vector<vector<int>>&st, int (*func)(int, int)){
    int n = a.size();
    for(int i=0; i<n; i++){
        st[i][0] = a[i];
    }
    for(int j=1; j<30; j++){
        for(int i=0; i+(1LL<<j)-1<n; i++){
            st[i][j] = func(st[i][j-1], st[i+(1LL<<(j-1))][j-1]);
        }
    }
}
int query(int l, int r, vector<vector<int>>&st, int (*func)(int, int)){
    int j = log2(r - l + 1);
    return func(st[l][j], st[r-(1LL<<j)+1][j]);
}

vector<vector<int>> stM(n, vector<int>(30));
init_sparse(a, stM, _max);
query(l, r, stM, _max); // 0-indexed