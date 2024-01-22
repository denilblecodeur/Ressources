from collections import defaultdict, deque
from itertools import product

class Automata:
    def __init__(self, transitions_mapping):
        # Non-deterministic delta application, delta : Q × ∑ → P(Q)
        self.transitions = defaultdict(lambda: defaultdict(set))
        for start, letter, end in transitions_mapping:
            self.transitions[start][letter].add(end)

    def __mul__(self, other):
        if not isinstance(other, Automata):
            raise RuntimeError('Cannot take the cartesian product with something else than an Automata!')
        
        transitions_mapping = []
        for state_1, state_2 in product(self.transitions.keys(), other.transitions.keys()):
            letters = set(self.transitions[state_1].keys()) & set(other.transitions[state_2].keys())
            for letter in letters:
                transitions_mapping += [((state_1, state_2), letter, (target_1, target_2)) for target_1, target_2 in product(self.transitions[state_1][letter], other.transitions[state_2][letter])]

        return Automata(transitions_mapping)

def compute_reset_sequence_between(aut, a, b):
    better = aut*aut
    queue = deque([((a, b), str())])
    visited = {s: False for s in better.transitions.keys()}

    while queue:
        cur, path = queue.pop()
        
        visited[cur] = True

        for letter, ends in better.transitions[cur].items():
            for end in ends:
                if end[0] == end[1]:
                    return path + letter
                elif end in visited and not visited[end]:
                    queue.appendleft((end, path + letter))

    return "fail"
    
def main():
    N, M = list(map(int, input().split()))
    X, Y = list(map(int, input().split()))
    tunnels = [None] * M
    for i in range(M):
        # start_state letter end_state
        # delta(letter, start_state) = end_state
        tunnels[i] = input().split()
        # integers
        tunnels[i][0] = int(tunnels[i][0])
        tunnels[i][2] = int(tunnels[i][2])

    aut = Automata(tunnels)
    print(compute_reset_sequence_between(aut, X, Y))

main()