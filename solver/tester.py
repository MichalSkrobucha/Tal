from time import time
from typing import Callable

from solver.solverLogic import solverLogic

BRUTE = 0
GREEDY = 1
DYNAMIC = 2
FPTAS = 3


def testAlgo(algo: int, capacity: int, data: list[list[float | int]]) -> None:
    logic: solverLogic = solverLogic()

    algorithm: Callable[[], (list[int], list[int])] = lambda: ([], [0, 0])

    match algo:
        case 0:
            print('Brute', end=' ')
            algorithm = logic.brute
        case 1:
            print('Greedy')
            algorithm = logic.greedy
        case 2:
            print('Dynamic')
            algorithm = logic.dynamic
        case 3:
            print('FPTAS')
            algorithm = logic.fptas

    logic.loadData(capacity, data)

    print(f'n = {len(data)}')

    chosen: list[int]
    complexity: list[int]

    chosen, complexity = algorithm()

    value: float = sum([data[i][0] for i in chosen])

    print(f'value = {value} ; complexity : time = {complexity[0]}, memory = {complexity[1]}')


def main() -> None:
    capacity: int = 10
    data: list[list[float | int]] = [[3.0, 5], [7.0, 4], [3.33, 11]]  # value, weight

    testAlgo(BRUTE, capacity, data)


if __name__ == '__main__':
    main()
