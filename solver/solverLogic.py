import _io
import sys
from itertools import combinations


class solverLogic:
    def __init__(self):
        self.capacity: float = 0.0
        self.items: list[list[float]] = []  # [value, weight]
        self.doLogs: bool = True
        self.logStream: list[_io.TextIOWrapper] = [sys.stdout]

    def loadData(self, capacity: float, items: list[list[float]]) -> None:
        self.capacity = capacity
        self.items = items

    def log(self, message: str, stream : list[_io.TextIOWrapper] = []) -> None:
        if self.doLogs:
            if len(stream) == 0:
                for s in self.logStream:
                    s.write(message + "\n")
            else:
                for s in stream:
                    s.write(message + "\n")

    def precise(self) -> (float, list[list[float]]):

        weightWasOKinAtLeastOne: bool = True
        maxValue: float = 0.0
        chosen: list[list[float]] = []

        self.log('Precise algorithm')

        for r in range(1, len(self.items) + 1):
            if not weightWasOKinAtLeastOne:
                break

            self.log(f'Checking subssets of size {r}')

            weightWasOKinAtLeastOne = False

            subsets: list[tuple[list[float], ...]] = combinations(self.items, r)

            for s in subsets:
                self.log(f'Subset {s}')

                weight: float = 0.0
                value: float = 0.0

                for v, w in s:
                    weight += w
                    value += v

                self.log(f'Value {value}, weight {weight}')

                if weight <= self.capacity:
                    weightWasOKinAtLeastOne = True

                    if value > maxValue:
                        chosen = list(s)
                        maxValue = value
                        self.log('Is most valueable set (so far)')

                else:
                    self.log(f'Not enough backpack capacity')

        return maxValue, chosen

    def greedy(self) -> (float, list[list[float]]):
        value: float = 0.0
        weight: float = 0.0
        densities: list[list[float]] = sorted([[v, w, v / w] for v, w in self.items], key=lambda x: x[2], reverse=True)
        chosen: list[list[float]] = []

        self.log('Greedy algorithm')
        self.log('Value, Weight, Density')
        for v, w, d in densities:
            self.log(f'({v, w, d})')

        for v, w, d in densities:
            if weight + w <= self.capacity:
                chosen.append([v, w])
                value += v
                weight += w

                self.log(f'Adding item ({v, w, d}), current value {value}, current weight {weight}')
            else:
                self.log(f'Item ({v, w, d}) won\'t fit in backpack')

        return value, chosen

    def fptas(self) -> (float, list[list[float]]):
        self.log("FPTAS function is WIP", [std.stderr])

        return 0.0, []
