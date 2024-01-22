def tarjan(G):
    n = len(G)
    SCC, S, P = [], [], []
    Q, state = list(range(n)), [0] * n
    while Q:
        node = Q.pop()
        if node < 0:
            d = state[~node] - 1
            if P[-1] > d:
                SCC.append(S[d:])
                del S[d:]; P.pop()
                for v in SCC[-1]:
                    state[v] = -1
        elif state[node] > 0:
            while P[-1] > state[node]:
                P.pop()
        elif state[node] == 0:
            S.append(node)
            P.append(len(S))
            state[node] = len(S)
            Q.append(~node)
            Q.extend(G[node])
    return SCC