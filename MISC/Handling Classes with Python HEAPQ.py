# Handling Classes with Python HEAPQ
# https://stackoverflow.com/questions/3954530/how-to-make-heapq-evaluate-the-heap-off-of-a-specific-attribute#answer-72330706

from heapq import *
from dataclasses import dataclass, field

@dataclass(order=True)
class State:
    state_trainCars: int = field(compare=True)
    state_route_mask: int = field(compare=False)
    state_cards: tuple = field(compare=False)

heap = [State(trainCars, (1 << numRoutes) - 1, cards)]
cur_state = heappop(heap)