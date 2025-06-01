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
            print('Greedy', end=' ')
            algorithm = logic.greedy
        case 2:
            print('Dynamic', end=' ')
            algorithm = logic.dynamic
        case 3:
            print('FPTAS', end=' ')
            algorithm = logic.fptas

    logic.loadData(capacity, data)

    print(f'n = {len(data)}')

    chosen: list[int]
    complexity: list[int]

    chosen, complexity = algorithm()

    value: float = sum([data[i][0] for i in chosen])

    print(f'value = {value} ; complexity : time = {complexity[0]}, memory = {complexity[1]}')


def testAllAlgos(capacity: int, data: list[list[float | int]]) -> None:
    testAlgo(BRUTE, capacity, data)
    testAlgo(GREEDY, capacity, data)
    testAlgo(DYNAMIC, capacity, data)
    testAlgo(FPTAS, capacity, data)


def main() -> None:
    # data : [value, weight]

    testAllAlgos(10, [[3.0, 5], [7.0, 4], [3.33, 11]])


if __name__ == '__main__':
    main()
