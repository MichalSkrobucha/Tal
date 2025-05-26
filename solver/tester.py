from solver.solverLogic import solverLogic
from time import time


def main() -> None:
    logic: solverLogic = solverLogic()

    capacity: int = 10
    data: list[list[float | int]] = [[3.0, 5], [7.0, 4], [3.33, 11]]  # value, weight

    n : int = len(data)
    print('n = ', n)
    print('Algorithm, value, time')

    logic.loadData(capacity, data)

    start : time = time()
    result : list[int] = logic.brute()
    end : time = time()
    value : float = sum([data[i][0] for i in result])
    print('Brute', value, end - start)

    start: time = time()
    result: list[int] = logic.greedy()
    end: time = time()
    value: float = sum([data[i][0] for i in result])
    print('Greedy', value, end - start)

    start: time = time()
    result: list[int] = logic.dynamic()
    end: time = time()
    value: float = sum([data[i][0] for i in result])
    print('Dynamic', value, end - start)

    start: time = time()
    result: list[int] = logic.fptas()
    end: time = time()
    value: float = sum([data[i][0] for i in result])
    print('FPTAS', value, end - start)



if __name__ == '__main__':
    main()
