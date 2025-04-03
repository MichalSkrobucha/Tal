import json
import sys

from PyQt6.QtWidgets import QMainWindow, QPushButton, QFileDialog, QGroupBox, QRadioButton, QLabel, QGridLayout, \
    QHBoxLayout

from solver.solverLogic import solverLogic


class solverApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.logic = solverLogic()

        # self.capacity: float = 0.0
        # self.items: list[list[float]] = []  # [value, weight]
        self.algorithm : int = 0 # 0-precise, 1-greedy

        self.readFile_button: QPushButton
        self.solve_button : QPushButton
        self.precise_radio : QRadioButton
        self.greedy_radio : QRadioButton

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('Solver')
        self.setFixedSize(500, 500)
        self.move(710, 270)

        self.readFile_button = QPushButton(self)
        self.readFile_button.setFixedSize(150, 40)
        self.readFile_button.move(75, 25)
        self.readFile_button.setText('Read from file')
        self.readFile_button.clicked.connect(self.readFile)
        self.readFile_button.show()

        self.solve_button = QPushButton(self)
        self.solve_button.setFixedSize(150, 40)
        self.solve_button.move(275, 25)
        self.solve_button.setText('Solve')
        self.solve_button.clicked.connect(self.solve)
        self.solve_button.setEnabled(False)
        self.solve_button.show()

        self.chooseAlgorithm_label = QLabel(self)
        self.chooseAlgorithm_label.setFixedSize(100, 40)
        self.chooseAlgorithm_label.move(75, 75)
        self.chooseAlgorithm_label.setText('Choose algorithm:')
        self.chooseAlgorithm_label.show()

        self.precise_radio = QRadioButton(self)
        self.precise_radio.setFixedSize(75, 35)
        self.precise_radio.move(225, 75)
        self.precise_radio.setText('Precise')
        self.precise_radio.clicked.connect(self.preciseClicked)
        self.precise_radio.setChecked(True)
        self.precise_radio.show()

        self.greedy_radio = QRadioButton(self)
        self.greedy_radio.setFixedSize(75, 35)
        self.greedy_radio.move(325, 75)
        self.greedy_radio.setText('Greedy')
        self.greedy_radio.clicked.connect(self.greedyClicked)
        self.greedy_radio.show()


    def solve(self) -> None:
        value : float = 0.0
        chosen : list[list[float]] = []

        match self.algorithm:
            case 0:
                self.precise_radio.setEnabled(False)
                self.greedy_radio.setEnabled(False)

                value, chosen = self.logic.precise()

            case 1:
                self.precise_radio.setEnabled(False)
                self.greedy_radio.setEnabled(False)

                value, chosen = self.logic.greedy()

            case _:
                pass

        self.precise_radio.setEnabled(True)
        self.greedy_radio.setEnabled(True)

    def readFile(self) -> None:
        openFilePath: str = QFileDialog.getOpenFileName(self, 'Open File', './', '.json (*.json) ;; .* (*.*)')[0]

        if openFilePath:
            with open(openFilePath, 'r', encoding='utf-8') as file:
                data: dict = json.load(file)

                if data['capacity'] < 0.0:
                    print(f'Negative capacity', file=sys.stderr)
                    return

                for v, w in data['items']:
                    if float(v) < 0.0:
                        print(f'Data contains item with negative value: ({v}, {w})', file=sys.stderr)
                        return

                    if float(w) < 0.0:
                        print(
                            f'Data contains item with negative weight: ({v}, {w})',
                            file=sys.stderr)
                        return

                # self.capacity = data['capacity']
                # self.items = data['items']

                self.logic.loadData(data['capacity'], data['items'])
        else:
            print('Something went wrong', file=sys.stderr)
            return

        self.solve_button.setEnabled(True)

    def preciseClicked(self, clicked : bool) -> None:
        if clicked:
            self.algorithm = 0

    def greedyClicked(self, clicked : bool) -> None:
        if clicked:
            self.algorithm = 1