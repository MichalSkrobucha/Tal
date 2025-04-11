import sys
from itertools import chain, combinations


class solverLogic:
    def __init__(self):
        self.capacity: float = 0.0
        self.items: list[list[float]] = []  # [value, weight]

    def loadData(self, capacity: float, items: list[list[float]]) -> None:
        self.capacity = capacity
        self.items = items

    def precise(self) -> (float, list[list[float]]):

        weightWasOKinAtLeastOne: bool = True
        maxValue: float = 0.0
        chosen: list[list[float]] = []

        print('Precise algorithm')

        for r in range(1, len(self.items) + 1):
            if not weightWasOKinAtLeastOne:
                break

            print(f'Checking subssets of size {r}')

            weightWasOKinAtLeastOne = False

            subsets: list[tuple[list[float], ...]] = combinations(self.items, r)

            for s in subsets:
                print(f'Subset {s}')

                weight: float = 0.0
                value: float = 0.0

                for v, w in s:
                    weight += w
                    value += v

                print(f'Value {value}, weight {weight}')

                if weight <= self.capacity:
                    weightWasOKinAtLeastOne = True

                    if value > maxValue:
                        chosen = s
                        maxValue = value
                        print('Is most valueable set (so far)')

                else:
                    print(f'Not enough backpack capacity')

        return maxValue, chosen

    def greedy(self) -> (float, list[list[float]]):
        value: float = 0.0
        weight: float = 0.0
        densities: list[list[float]] = sorted([[v, w, v / w] for v, w in self.items], key=lambda x: x[2], reverse=True)
        chosen: list[list[float]] = []

        print('Greedy algorithm')
        print('Value, Weight, Density')
        for v, w, d in densities:
            print(f'({v, w, d})')

        for v, w, d in densities:
            if weight + w <= self.capacity:
                chosen.append([v, w])
                value += v
                weight += w

                print(f'Adding item ({v, w, d}), current value {value}, current weight {weight}')
            else:
                print(f'Item ({v, w, d}) won\'t fit in backpack')

        return value, chosen
