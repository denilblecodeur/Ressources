from sys import stdin, stdout

class NoSolution(Exception):
    pass

def topological_order(graph):
    n = len(graph)
    order = []
    NOT_PROCESSED, IN_PROCESS, PROCESSED = 0, 1, 2
    state = [NOT_PROCESSED] * n
    times_seen = [-1] * n
    for start in range(n):
        if state[start] == NOT_PROCESSED:
            times_seen[start] = 0
            to_visit = [start]
            while to_visit:
                node = to_visit[-1]
                state[node] = IN_PROCESS
                children = graph[node]
                if times_seen[node] == len(children):
                    to_visit.pop()
                    order.append(node + 1)
                    state[node] = PROCESSED
                else:
                    child = children[times_seen[node]]
                    times_seen[node] += 1
                    if state[child] == IN_PROCESS:
                        raise NoSolution
                    if times_seen[child] == -1:
                        times_seen[child] = 0
                        to_visit.append(child)
    return order[::-1]


if __name__=="__main__":

    n, m = map(int,stdin.readline().split())
    graph = [[] for _ in range(n)]
    for _ in range(m):
        a,b = map(int,stdin.readline().split())
        graph[a-1].append(b-1)
    
    try:
        toposort = topological_order(graph)
        stdout.write(' '.join(map(str,toposort)) + '\n')
    except:
        stdout.write('IMPOSSIBLE\n')