from sys import stdin, stdout
input = stdin.readline

def main():
    def floyd_warshall(n, dist):     
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][j] < dist[i][k] * dist[k][j]:
                        dist[i][j] = dist[i][k] * dist[k][j]
        for i in range(n):
            if dist[i][i] > 1:
                return 'Yes'
        return 'No'

    ans = []
    t_case = 0
    while True:
        t_case += 1
        n = int(input())
        if n == 0:
            stdout.write('\n'.join(ans) + '\n')
            return
        conv = {}
        for i in range(n):
            currency = input().rstrip('\n')
            conv[currency] = i
        dist = [[0] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 1
        for _ in range(int(input())):
            curr1, exchange_rate, curr2 = input().rstrip('\n').split()
            dist[conv[curr1]][conv[curr2]] = float(exchange_rate)
        input()
        ans.append('Case {}: {}'.format(t_case, floyd_warshall(n, dist)))

main()