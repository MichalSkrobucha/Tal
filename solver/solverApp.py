import json
import sys
from typing import Callable

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QMainWindow, QPushButton, QFileDialog, QRadioButton, QLabel, QScrollArea, QWidget, \
    QVBoxLayout, QSlider, QLineEdit

from solver.solverLogic import solverLogic


class solverApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.items: list[list[float]] = []  # value, weight

        self.logic = solverLogic()

        self.algorithm: Callable[[], list[int]] = self.logic.brute

        self.readFile_button: QPushButton
        self.solve_button: QPushButton
        self.brute_radio: QRadioButton
        self.greedy_radio: QRadioButton
        self.dynamic_radio: QRadioButton
        self.fptas_radio: QRadioButton
        self.epsilon_slider: QSlider
        self.epsilon_ledit: QLineEdit
        self.chosen_label: QLabel
        self.chosenItems_scroll: QScrollArea
        self.scrollable_widget: QWidget
        self.content: QVBoxLayout
        self.chosenItems_labels: list[QLabel] = []

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

        self.brute_radio = QRadioButton(self)
        self.brute_radio.setFixedSize(90, 35)
        self.brute_radio.move(185, 75)
        self.brute_radio.setText('Brute force')
        self.brute_radio.clicked.connect(self.bruteClicked)
        self.brute_radio.setChecked(True)
        self.brute_radio.show()

        self.greedy_radio = QRadioButton(self)
        self.greedy_radio.setFixedSize(75, 35)
        self.greedy_radio.move(275, 75)
        self.greedy_radio.setText('Greedy')
        self.greedy_radio.clicked.connect(self.greedyClicked)
        self.greedy_radio.show()

        self.dynamic_radio = QRadioButton(self)
        self.dynamic_radio.setFixedSize(75, 35)
        self.dynamic_radio.move(350, 75)
        self.dynamic_radio.setText('Dynamic')
        self.dynamic_radio.clicked.connect(self.dynamicClicked)
        self.dynamic_radio.show()

        self.fptas_radio = QRadioButton(self)
        self.fptas_radio.setFixedSize(75, 35)
        self.fptas_radio.move(425, 75)
        self.fptas_radio.setText('FPTAS')
        self.fptas_radio.clicked.connect(self.fptasClicked)
        self.fptas_radio.show()

        self.epsilon_title = QLabel(self)
        self.epsilon_title.setFixedSize(50, 20)
        self.epsilon_title.move(25, 110)
        self.epsilon_title.setText('Epsilon')
        self.epsilon_title.show()

        self.epsilon_slider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.epsilon_slider.setFixedSize(300, 20)
        self.epsilon_slider.move(75, 110)
        self.epsilon_slider.setMinimum(0)
        self.epsilon_slider.setMaximum(1000)
        self.epsilon_slider.setTickInterval(1)
        self.epsilon_slider.setValue(500)
        self.epsilon_slider.sliderMoved.connect(self.epsilonMoved)
        self.epsilon_slider.sliderPressed.connect(self.epsilonPressed)
        self.epsilon_slider.show()
        self.epsilon_slider.setEnabled(False)

        self.epsilon_ledit = QLineEdit(self)
        self.epsilon_ledit.setFixedSize(50, 20)
        self.epsilon_ledit.move(400, 110)
        self.epsilon_ledit.setValidator(QDoubleValidator(0.000, 1.000, 3))
        self.epsilon_ledit.setText('0.500')
        self.epsilon_ledit.textEdited.connect(self.epsilonEdited)
        self.epsilon_ledit.show()
        self.epsilon_ledit.setEnabled(False)

        self.chosen_label = QLabel(self)
        self.chosen_label.setFixedSize(400, 40)
        self.chosen_label.move(75, 130)
        self.chosen_label.setText('Current items (value, weight)')
        self.chosen_label.show()

        self.chosenItems_scroll = QScrollArea(self)
        self.chosenItems_scroll.setMinimumSize(450, 300)
        self.chosenItems_scroll.move(25, 175)
        self.chosenItems_scroll.setWidgetResizable(True)
        self.chosenItems_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.chosenItems_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.chosenItems_scroll.show()

        self.scrollable_widget = QWidget()
        self.scrollable_widget.setMinimumSize(450, 300)
        self.content = QVBoxLayout(self.scrollable_widget)

        self.chosenItems_scroll.setWidget(self.scrollable_widget)

    def solve(self) -> None:
        self.brute_radio.setEnabled(False)
        self.greedy_radio.setEnabled(False)
        self.dynamic_radio.setEnabled(False)
        self.solve_button.setEnabled(False)

        chosen: list[list[float]] = [self.items[i] for i in self.algorithm()]
        value: float = sum([v for v, _ in chosen])

        self.brute_radio.setEnabled(True)
        self.greedy_radio.setEnabled(True)
        self.dynamic_radio.setEnabled(True)
        self.solve_button.setEnabled(True)

        self.removeItems()
        self.addItems(chosen)

        self.chosen_label.setText(f'Chosen items (value, weight) \t Computed value: {value}')

    def removeItems(self) -> None:
        # removing old items
        current: QLabel

        for _ in range(len(self.chosenItems_labels)):
            current = self.chosenItems_labels[0]
            del self.chosenItems_labels[0]
            current.deleteLater()

    def addItems(self, items: list[list[float]]) -> None:
        for v, w in items:
            current = QLabel(self.scrollable_widget)
            current.setFixedSize(150, 40)
            current.move(25, 50 * len(self.chosenItems_labels) + 10)
            current.setText(f'({v} ; {w})')
            current.show()
            self.chosenItems_labels.append(current)

        if len(self.chosenItems_labels) >= 6:
            self.scrollable_widget.setMinimumSize(450, 50 * len(self.chosenItems_labels))
        else:
            self.scrollable_widget.setMinimumSize(450, 300)

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

                self.items = data['items']
                self.logic.loadData(data['capacity'], data['items'])

                self.removeItems()
                self.addItems(data['items'])

                self.chosen_label.setText(f'Current items (value, weight) \t Capacity {data["capacity"]}')

        else:
            print('Something went wrong', file=sys.stderr)
            return

        self.solve_button.setEnabled(True)

    def bruteClicked(self, clicked: bool) -> None:
        if clicked:
            self.algorithm = self.logic.brute

        self.epsilon_slider.setEnabled(False)
        self.epsilon_ledit.setEnabled(False)

    def greedyClicked(self, clicked: bool) -> None:
        if clicked:
            self.algorithm = self.logic.greedy

        self.epsilon_slider.setEnabled(False)
        self.epsilon_ledit.setEnabled(False)

    def dynamicClicked(self, clicked: bool) -> None:
        if clicked:
            self.algorithm = self.logic.dynamic

        self.epsilon_slider.setEnabled(False)
        self.epsilon_ledit.setEnabled(False)

    def fptasClicked(self, clicked: bool) -> None:
        if clicked:
            self.algorithm = self.logic.fptas

        self.epsilon_slider.setEnabled(True)
        self.epsilon_ledit.setEnabled(True)

    def epsilonMoved(self, ticks: int) -> None:
        self.epsilon_ledit.setText(str(ticks / 1000))
        self.logic.epsilon = ticks / 1000

    def epsilonPressed(self) -> None:
        self.epsilon_ledit.setText(str(self.epsilon_slider.value() / 1000))
        self.logic.epsilon = self.epsilon_slider.value() / 1000

    def epsilonEdited(self, newStr: str) -> None:
        self.epsilon_slider.setValue(int(1000 * float(newStr)))
        self.logic.epsilon = float(newStr)
