from itertools import chain, combinations


class solverLogic:
    def __init__(self):
        self.capacity: float = 0.0
        self.items: list[list[float]] = []  # [value, weight]

    def loadData(self, capacity: float, items: list[list[float]]) -> None:
        self.capacity = capacity
        self.items = items

    def precise(self) -> (float, list[float]):
        subsets: list[list[list[float]]] = list(
            chain.from_iterable(combinations(self.items, r) for r in range(len(self.items) + 1)))

        maxValue: float = 0.0
        chosen: list[list[float]] = []

        for s in subsets:
            weight: float = 0.0
            value: float = 0.0

            for v, w in s:
                weight += w
                value += v

            if weight <= self.capacity and value > maxValue:
                chosen = s
                maxValue = value

        return maxValue, chosen

    def greedy(self) -> (float, list[float]):
        value: float = 0.0
        weight: float = 0.0
        densities: list[list[float]] = sorted([[v, w, v / w] for v, w in self.items], key=lambda x: x[2], reverse=True)
        chosen: list[list[float]] = []

        for v, w, d in densities:
            if weight + w <= self.capacity:
                chosen.append([v, w])
                value += v
                weight += w

        return value, chosen
