#include <bits/stdc++.h>
using namespace std;

struct SD {
    int N, len;
	vector<int> a, b, c;
	SD(int n) {
        N = n;
        len = (int) sqrt (N + 0.) + 1;
        a = vector<int>(N, 0);
        b = vector<int>(len, 0);
        c = vector<int>(len, 0);
    }
	int query(int l, int r) {
        assert(0<=l && r<N && l<=r);
        int c_l = l / len, c_r = r / len;
        int sum = 0;
        if(c_l == c_r){
            for(int i=l; i<=r; i++)
                sum += a[i];
            sum += b[c_l] * (r - l + 1);
        }
        else{
            for(int i=l; i<(c_l+1)*len; i++)
                sum += a[i];
            sum += b[c_l] * ((c_l+1)*len - l);
            for(int i=c_l+1; i<=c_r-1; i++)
                sum += b[i] * len + c[i];
            for(int i=c_r*len; i<=r; i++)
                sum += a[i];
            sum += b[c_r] * (r - c_r*len + 1);
        }
        return sum;
    }
    void set(int l, int r) {
        assert(0<=l && r<N && l<=r);
        int c_l = l / len, c_r = r / len;
        if(c_l == c_r){
            for(int i=l; i<=r; i++)
                a[i] += 1;
            c[c_l] += r - l + 1;
        }
        else{
            for(int i=l; i<(c_l+1)*len; i++)
                a[i] += 1;
            c[c_l] += (c_l+1)*len - l;
            for(int i=c_l+1; i<=c_r-1; i++)
                b[i] += 1;
            for(int i=c_r*len; i<=r; i++)
                a[i] += 1;
            c[c_r] += r - c_r*len + 1;
        }
    }
};

int main(){
    int n; cin >> n;
    SD white(n);
    SD black(n);
    int t; cin >> t;
    while(t--){
        int q, l, r; cin >> q >> l >> r;
        if(q){
            black.set(l, r);
            cout << black.query(0, n - 1) << endl;
        }else{
            white.set(l, r);
            cout << white.query(0, n - 1) << endl;
        }
    }
}