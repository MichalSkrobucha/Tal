import json
import sys
from random import expovariate, normalvariate

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator, QScrollEvent
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QScrollArea, QWidget, QVBoxLayout, \
    QSizePolicy


class generatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.capacity: float = 0.0
        self.items: list[list[float]] = []  # [value, weight]

        self.readFile_button: QPushButton
        self.saveFile_button: QPushButton
        self.randomize_button: QPushButton
        self.backpackCapacity_label: QLabel
        self.backpackCapacity_ledit: QLineEdit
        self.itemValue_label: QLabel
        self.itemWeight_label: QLabel
        self.itemData_scroll : QScrollArea
        self.scrollable_widget : QWidget
        self.itemValues_ledits: list[QLineEdit] = []
        self.itemWeights_ledits: list[QLineEdit] = []
        self.removeitem_buttons: list[QPushButton] = []
        self.addItem_button: QPushButton

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('Generator')
        self.setFixedSize(500, 500)
        self.move(710, 270)

        self.readFile_button = QPushButton(self)
        self.readFile_button.setFixedSize(130, 40)
        self.readFile_button.move(30, 20)
        self.readFile_button.setText('Read from file')
        self.readFile_button.clicked.connect(self.readFile)
        self.readFile_button.show()

        self.saveFile_button = QPushButton(self)
        self.saveFile_button.setFixedSize(130, 40)
        self.saveFile_button.move(185, 20)
        self.saveFile_button.setText('Save to file')
        self.saveFile_button.clicked.connect(self.saveFile)
        self.saveFile_button.show()

        self.randomize_button = QPushButton(self)
        self.randomize_button.setFixedSize(130, 40)
        self.randomize_button.move(340, 20)
        self.randomize_button.setText('Randomize')
        self.randomize_button.clicked.connect(self.randomize)
        self.randomize_button.show()

        self.backpackCapacity_label = QLabel(self)
        self.backpackCapacity_label.setFixedSize(150, 40)
        self.backpackCapacity_label.move(75, 70)
        self.backpackCapacity_label.setText('Backpack capacity: ')
        self.backpackCapacity_label.show()

        self.backpackCapacity_ledit = QLineEdit(self)
        self.backpackCapacity_ledit.setFixedSize(150, 40)
        self.backpackCapacity_ledit.move(275, 70)
        self.backpackCapacity_ledit.setText('0,0')
        self.backpackCapacity_ledit.setValidator(QDoubleValidator(0.0, sys.float_info.max, 16))
        self.backpackCapacity_ledit.textEdited.connect(self.capacityEdited)
        self.backpackCapacity_ledit.show()

        self.itemValue_label = QLabel(self)
        self.itemValue_label.setFixedSize(150, 40)
        self.itemValue_label.move(75, 120)
        self.itemValue_label.setText('Item Value:')
        self.itemValue_label.show()

        self.itemWeight_label = QLabel(self)
        self.itemWeight_label.setFixedSize(150, 40)
        self.itemWeight_label.move(275, 120)
        self.itemWeight_label.setText('Item Weight:')
        self.itemWeight_label.show()

        self.itemData_scroll = QScrollArea(self)
        self.itemData_scroll.setMinimumSize(450, 300)
        self.itemData_scroll.move(25, 170)
        self.itemData_scroll.setWidgetResizable(True)
        self.itemData_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.itemData_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.itemData_scroll.show()

        self.scrollable_widget = QWidget()
        self.scrollable_widget.setMinimumSize(450, 300)
        self.content : QVBoxLayout = QVBoxLayout(self.scrollable_widget)

        self.itemData_scroll.setWidget(self.scrollable_widget)

        self.itemValues_ledits: list[QLineEdit]
        self.itemWeights_ledits: list[QLineEdit]
        self.removeitem_buttons: list[QPushButton]

        self.addItem_button = QPushButton(self.scrollable_widget)
        self.addItem_button.setFixedSize(40, 40)
        self.addItem_button.move(375, 10)
        self.addItem_button.setText('+')
        self.addItem_button.clicked.connect(self.addItem)
        self.addItem_button.show()

        self.addItem()
        # self.addItem()
        # self.addItem()
        # self.addItem()
        # self.addItem()
        # self.addItem()
        # self.addItem()
        # self.addItem()


    def setupItems(self) -> None:
        current: int = len(self.itemWeights_ledits)
        toBe: int = len(self.items)

        if toBe >= current:
            for _ in range(toBe - current):
                self.addItem()
        else:
            pass
            for _ in range(current - toBe):
                self.removeItem(toBe)

        for i in range(toBe):
            self.itemValues_ledits[i].setText(str(self.items[i][0]))
            self.itemWeights_ledits[i].setText(str(self.items[i][1]))

    def removeItem(self, id: int) -> None:
        # usunięcie itemu (value, weight, removeButton) o wskazanym id
        delV: QLineEdit = self.itemValues_ledits[id]
        delW: QLineEdit = self.itemWeights_ledits[id]
        delR: QPushButton = self.removeitem_buttons[id]
        del self.itemValues_ledits[id]
        del self.itemWeights_ledits[id]
        del self.removeitem_buttons[id]
        delV.deleteLater()
        delW.deleteLater()
        delR.deleteLater()

        # przesunięcie niższych itemów w górę
        for i in range(len(self.itemValues_ledits)):
            self.itemValues_ledits[i].move(25, 10 + 50 * i)

        for i in range(len(self.itemWeights_ledits)):
            self.itemWeights_ledits[i].move(200, 10 + 50 * i)

        for i in range(len(self.removeitem_buttons)):
            self.removeitem_buttons[i].move(375, 10 + 50 * i)

        self.addItem_button.move(375, 10 + 50 * len(self.itemValues_ledits))

        if len(self.removeitem_buttons) < 5:
            self.scrollable_widget.setMinimumSize(450, 300)
        else:
            self.scrollable_widget.setMinimumSize(450, 50 * (len(self.removeitem_buttons) + 1))

    def removeItemSlot(self, ) -> None:
        self.removeItem(self.removeitem_buttons.index(self.sender()))

    def addItem(self) -> None:
        self.itemValues_ledits.append(QLineEdit(self.scrollable_widget))
        self.itemValues_ledits[-1].setFixedSize(150, 40)
        self.itemValues_ledits[-1].move(25, 50 * len(self.itemValues_ledits) - 40)
        self.itemValues_ledits[-1].setText('0,0')
        self.itemValues_ledits[-1].setValidator(QDoubleValidator(0.0, sys.float_info.max, 16))
        self.itemValues_ledits[-1].textEdited.connect(self.valueEditedSlot)
        self.itemValues_ledits[-1].show()

        self.itemWeights_ledits.append(QLineEdit(self.scrollable_widget))
        self.itemWeights_ledits[-1].setFixedSize(150, 40)
        self.itemWeights_ledits[-1].move(200, 50 * len(self.itemWeights_ledits) - 40)
        self.itemWeights_ledits[-1].setText('0,0')
        self.itemWeights_ledits[-1].setValidator(QDoubleValidator(0.0, sys.float_info.max, 16))
        self.itemWeights_ledits[-1].textEdited.connect(self.weightEditedSlot)
        self.itemWeights_ledits[-1].show()

        self.removeitem_buttons.append(QPushButton(self.scrollable_widget))
        self.removeitem_buttons[-1].setFixedSize(40, 40)
        self.removeitem_buttons[-1].move(375, 50 * len(self.removeitem_buttons) - 40)
        self.removeitem_buttons[-1].setText('-')
        self.removeitem_buttons[-1].clicked.connect(self.removeItemSlot)
        self.removeitem_buttons[-1].show()

        self.items.append([0.0, 0.0])

        if len(self.removeitem_buttons) >= 5:
            self.scrollable_widget.setMinimumSize(450, 50 * (len(self.removeitem_buttons) + 1))

        self.addItem_button.move(375, 10 + 50 * len(self.itemValues_ledits))

        self.itemData_scroll.verticalScrollBar().setValue(self.itemData_scroll.verticalScrollBar().value() + 50)

    def capacityEdited(self, text: str) -> None:
        self.capacity = float(text.replace(',', '.'))

    def valueEditedSlot(self, text: str) -> None:
        id: int = self.itemValues_ledits.index(self.sender())
        self.items[id][0] = float(text.replace(',', '.'))

    def weightEditedSlot(self, text: str) -> None:
        id: int = self.itemWeights_ledits.index(self.sender())
        self.items[id][1] = float(text.replace(',', '.'))

    def readFile(self) -> None:
        openFilePath: str = QFileDialog.getOpenFileName(self, 'Open File', './', '.json (*.json) ;; .* (*.*)')[0]

        if openFilePath:
            with open(openFilePath, 'r', encoding='utf-8') as file:
                data: dict = json.load(file)

                for v, w in data['items']:
                    if float(v) < 0.0:
                        print(f'Data contains item with negative value: ({v}, {w})', file=sys.stderr)
                        return

                    if float(w) < 0.0:
                        print(
                            f'Data contains item with negative weight: ({v}, {w})',
                            file=sys.stderr)
                        return

                self.capacity = data['capacity']
                self.items = data['items']

                print(self.items)

                self.backpackCapacity_ledit.setText(str(self.capacity))
                self.setupItems()
        else:
            print('Something went wrong', file=sys.stderr)
            return

    def saveFile(self) -> None:
        saveFilePath: str = QFileDialog.getSaveFileName(self, 'Open File', './', '.json (*.json) ;; .* (*.*)')[0]

        if saveFilePath:
            with open(saveFilePath, 'w', encoding='utf-8') as file:
                json.dump(
                    {"capacity": self.capacity,
                     "items": self.items
                     },
                    file, ensure_ascii=False, indent=4)
        else:
            print('Something went wrong', file=sys.stderr)
            return

    def randomize(self) -> None:
        minWeight : float = sys.float_info.max
        sumWeight: float = 0.0

        for i, item in enumerate(self.items):
            item[0] = expovariate(0.5)
            weight : float = expovariate(0.5)
            item[1] = weight

            if weight < minWeight:
                minWeight = weight

            sumWeight += weight

            self.itemValues_ledits[i].setText(f'{item[0]:.3f}')
            self.itemWeights_ledits[i].setText(f'{item[1]:.3f}')


        self.capacity = normalvariate((sumWeight + minWeight) / 2, (sumWeight - minWeight) / 6)

        while self.capacity < 0.0:
            self.capacity = normalvariate((sumWeight + minWeight) / 2, (sumWeight - minWeight) / 6)

        self.backpackCapacity_ledit.setText(f'{self.capacity:.3f}')

