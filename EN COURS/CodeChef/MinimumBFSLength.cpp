#include<bits/stdc++.h>
using namespace std;

#define int long long

vector<vector<int> > g;
vector<int> mxd, mxd1;

void dfs1(int c, int p, int d){
    mxd[c] = d;
    mxd1[c] = d-1;
    for(auto h:g[c]){
        if(h!=p){
            dfs1(h,c,d+1);
            if(mxd[h]>mxd[c]){
                if(mxd[c] > d) mxd1[c] = mxd[c];
                mxd[c] = mxd[h];
            }
            else if(mxd[h]>mxd1[c]){
                mxd1[c] = mxd[h];
            }
        }
    }
}


int ans;

void dfs2(int c, int p, int d, int ancd){
    if(p!=-1){
        ans += max(1ll, (min(mxd[c], ancd)-d+1))*2;
    }

    for(auto h:g[c]){
        if(h!=p){
            int tancd;
            if(mxd[h]==mxd[c]) tancd = max(ancd, mxd1[c]);
            else tancd = max(ancd, mxd[c]);
            dfs2(h,c,d+1,tancd);
        }
    }
}

signed main(){

    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    #ifndef ONLINE_JUDGE
    freopen("input.txt", "r" , stdin);
    freopen("output.txt", "w" , stdout);
    #endif

    int tc;
    cin>>tc;

    while(tc--){
        int n;
        cin>>n;

        g.assign(n, vector<int>());
        mxd.assign(n, 0);
        mxd1.assign(n, 0);
        ans = 0;
        int x,y;

        for(int i=0; i<n-1; i++){
            cin>>x>>y;
            x--, y--;
            g[x].push_back(y);
            g[y].push_back(x);
        }

        dfs1(0,-1,0);
        dfs2(0,-1,0, -1);

        ans -= mxd[0];

        cout<<ans<<'\n';

    }

    return 0;
}