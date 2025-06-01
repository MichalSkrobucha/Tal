import math
from itertools import combinations


class solverLogic:
    def __init__(self):
        self.epsilon: float = 0.500

        self.capacity: float = 0.0
        self.items: list[list[float]] = []  # [value, weight]

    def loadData(self, capacity: float, items: list[list[float]]) -> None:
        self.capacity = capacity
        self.items = items

    def brute(self) -> (list[int], list[int]):
        time: int = 0
        memory: int = 0

        weightWasOKinAtLeastOne: bool = True
        maxValue: float = 0.0
        chosen: list[int] = []
        ids = range(len(self.items))

        # print('Precise algorithm')

        for r in range(1, len(self.items) + 1):
            if not weightWasOKinAtLeastOne:
                break

            # print(f'Checking subssets of size {r}')

            weightWasOKinAtLeastOne = False

            subsets: list[tuple[int]] = combinations(ids, r)

            if r > memory:
                memory = r

            for s in subsets:
                # print(f'Subset {s}')

                weight: float = 0.0
                value: float = 0.0

                for i in s:
                    value += self.items[i][0]
                    weight += self.items[i][1]

                    time += 1

                # print(f'Value {value}, weight {weight}')

                if weight <= self.capacity:
                    weightWasOKinAtLeastOne = True

                    if value > maxValue:
                        chosen = list(s)
                        maxValue = value
                        # print('Is most valueable set (so far)')

                else:
                    pass
                    # print(f'Not enough backpack capacity')

        return chosen, [time, memory]

    def greedy(self) -> (list[int], list[int]):
        time: int = 0
        memory: int = 0

        value: float = 0.0
        weight: float = 0.0
        densities: list[list[int | float]] = sorted([[i, v, w, v / w] for i, (v, w) in enumerate(self.items)],
                                                    key=lambda x: x[3], reverse=True)

        time += len(densities)
        memory = len(densities)

        chosen: list[int] = []

        # print('Greedy algorithm')
        # print('Value, Weight, Density')
        # for i, v, w, d in densities:
        #     pass
        #     print(f'({v, w, d})')

        for i, v, w, _ in densities:
            if weight + w <= self.capacity:
                chosen.append(i)
                value += v
                weight += w
                time += 1

                # print(f'Adding item ({v, w, d}), current value {value}, current weight {weight}')
            else:
                pass
                # print(f'Item ({v, w, d}) won\'t fit in backpack')

        return chosen, [time, memory]

    def dynamic(self) -> (list[int], list[int]):
        time: int = 0
        memory: int = 0

        capacity: int = math.floor(self.capacity)
        items: list[list[float | int]] = [[v, math.ceil(w)] for v, w in self.items]
        time += len(items)

        scale: int = math.gcd(*[w for _, w in items])
        if scale > 1:
            capacity //= scale
            for t in items:
                t[1] //= scale

        n: int = len(items)

        # maksymalna wartość dla pojemności i odpowiednie przedmioty
        dp: list[float] = [0.0] * (capacity + 1)
        chosen = [[] for _ in range(capacity + 1)]

        for i in range(n):
            v, w = items[i]
            # od tyłu - nie nadpisujemy wyników z poprzedniego kroku
            for c in range(capacity, w - 1, -1):
                if dp[c - w] + v > dp[c]:
                    dp[c] = dp[c - w] + v
                    chosen[c] = chosen[c - w] + [i]
                    time += 1

        memory = sum([len(c) for c in chosen])

        return chosen[capacity], [time, memory]

    def fptas(self) -> (list[int], list[int]):
        time: int = 0
        memory: int = 0

        items: list[list[float]] = [[v, w] for v, w in self.items]

        maxValue: float = max(*[w for _, w in self.items])
        K: float = self.epsilon * maxValue / len(items)
        newItems: list[list[int]] = [[float(math.floor(v / K)), math.ceil(w)] for v, w in items]

        time = memory = len(newItems)

        chosen: list[int]
        complexity: list[int]

        self.items = newItems
        chosen, complexity = self.dynamic()
        self.items = items

        return chosen, [complexity[0] + time, complexity[1] + memory]
