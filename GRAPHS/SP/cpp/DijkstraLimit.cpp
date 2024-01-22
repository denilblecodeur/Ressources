//g++ -std=c++17 -o main main.cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int t, n, m, a, b;
ll p, s, profit[801], weight[801][801];
pair<ll, ll> dp[801][801];

ll solve(vector<vector<int> > graph){
    priority_queue<pair<pair<ll,ll>,pair<int,int> > >heap;
    heap.push({{0, p}, {0, 0}});
    dp[0][0] = {0, p};
    while(heap.size()){
        ll repr_cnt = -heap.top().first.first, money = heap.top().first.second;
        int lastmax = heap.top().second.first, node = heap.top().second.second;
        heap.pop();
        if(profit[node] > profit[lastmax])
            lastmax = node;
        if(node == n - 1)
            return repr_cnt;
        for(auto neigh : graph[node]){
            ll w = weight[node][neigh];
            ll needed = 0, m = money;
            if(w > m){
                needed = ceil((w - m) / (double)profit[lastmax]);
                m += needed * profit[lastmax];
            }
            m -= w;
            ll r = repr_cnt + needed;
            if((dp[neigh][lastmax].first == -1) || (dp[neigh][lastmax].first > r) || (dp[neigh][lastmax].second < m)){
                dp[neigh][lastmax] = {r, m};
                heap.push({{-r, m}, {lastmax, neigh}});
            }
        }
    }
    return -1;
}

int main(){
    ios_base::sync_with_stdio(false); cin.tie(NULL);
    cin >> t;
    while(t--){
        cin >> n >> m >> p;
        for(int i=0; i<n; i++){
            cin >> profit[i];
            fill(weight[i], weight[i] + 801, -1);
            fill(dp[i], dp[i] + 801, make_pair(-1, -1));
        }
        vector<vector<int> > graph(n);
        for(int i=0; i<m; i++){
            cin >> a >> b >> s;
            a--; b--;
            if(weight[a][b] == -1){
                graph[a].push_back(b);
                weight[a][b] = s;
            }else{
                weight[a][b] = min(weight[a][b], s);
            }
        }
        cout << solve(graph) << endl;
    }
}