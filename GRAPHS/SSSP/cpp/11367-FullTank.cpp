//g++ -std=c++17 -o main main.cpp
#include <bits/stdc++.h>
using namespace std;

int t, n, m, a, b, c, fuel_price[1005], weight[1005][1005], dp[1005][105];

int dijkstra(int start, int target, int capa, vector<vector<int> > graph){
    for(int i=0; i<n; i++)
        fill(dp[i], dp[i] + 105, -1);
    priority_queue <pair<pair<int, int>, pair<int, int> > > heap;
    int curcost, fuel, city;
    heap.push({{0, 0}, {start, start}});
    while(heap.size()){
        curcost = -heap.top().first.first;
        fuel = heap.top().first.second;
        city = heap.top().second.first;
        heap.pop();
        if(city == target)
            return curcost;
        for(auto next_city : graph[city]){
            int newfuel = fuel - weight[city][next_city];
            if(newfuel >= 0 && (dp[next_city][newfuel] == -1 || dp[next_city][newfuel] > curcost)){
                dp[next_city][newfuel] = curcost;
                heap.push({{-curcost, newfuel}, {next_city, next_city}});
            }
        }
        for(int unit = 1; unit <= capa - fuel; unit++){
            int newcost = curcost + fuel_price[city] * unit;
            int newfuel = fuel + unit;
            if(dp[city][newfuel] == -1 || dp[city][newfuel] > newcost){
                dp[city][newfuel] = newcost;
                heap.push({{-newcost, newfuel}, {city, city}});
            }
        }
    }
    return -1;
}

int main(){
    ios_base::sync_with_stdio(false); cin.tie(0);
    cin >> n >> m;
    for(int i=0; i<n; i++){
        fill(weight[i], weight[i] + 1005, -1);
        cin >> fuel_price[i];
    }
    vector<vector<int> > graph(n);
    for(int i=0; i<m; i++){
        cin >> a >> b >> c;
        graph[a].push_back(b);
        graph[b].push_back(a);
        if((weight[a][b] == -1) || (c < weight[a][b]))
            weight[a][b] = weight[b][a] = c;
    }
    cin >> t;
    while(t--){
        cin >> a >> b >> c;
        int ans = dijkstra(b, c, a, graph);
        if(ans >= 0) cout << ans << endl;
        else cout << "impossible" << endl;
    }
}