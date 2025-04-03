

class solverLogic:
    def __init__(self):
        self.capacity: float = 0.0
        self.items: list[list[float]] = []  # [value, weight]

    def loadData(self, capacity : float, items : list[list[float]]) -> None:
        self.capacity = capacity
        self.items = items

    def precise(self) -> (float, list[float]):
        print('solving with precise algorithm')
        return 0.0, []

    def greedy(self) -> (float, list[float]):
        print('solving with greedy algorithm')
        return 0.0, []