import json
import sys

from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog


class generatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.capacity: float = 0.0
        self.items: list[list[float]] = []  # [value, weight]

        self.readFile_button: QPushButton
        self.saveFile_button: QPushButton
        self.backpackCapacity_label: QLabel
        self.backpackCapacity_ledit: QLineEdit
        self.itemValue_label: QLabel
        self.itemValues_ledits: list[QLineEdit] = []
        self.itemWeight_label: QLabel
        self.itemWeights_ledits: list[QLineEdit] = []
        self.addItem_button: QPushButton
        self.removeitem_buttons: list[QPushButton] = []

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('Generator')
        self.setFixedSize(500, 500)
        self.move(710, 270)

        self.readFile_button = QPushButton(self)
        self.readFile_button.setFixedSize(150, 40)
        self.readFile_button.move(75, 20)
        self.readFile_button.setText('Read from file')
        self.readFile_button.clicked.connect(self.readFile)
        self.readFile_button.show()

        self.saveFile_button = QPushButton(self)
        self.saveFile_button.setFixedSize(150, 40)
        self.saveFile_button.move(275, 20)
        self.saveFile_button.setText('Save to file')
        self.saveFile_button.clicked.connect(self.saveFile)
        self.saveFile_button.show()

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

        self.addItem_button = QPushButton(self)
        self.addItem_button.setFixedSize(40, 40)
        self.addItem_button.move(450, 220)
        self.addItem_button.setText('+')
        self.addItem_button.clicked.connect(self.addItem)
        self.addItem_button.show()

        self.itemValues_ledits: list[QLineEdit]
        self.itemWeights_ledits: list[QLineEdit]
        self.removeitem_buttons: list[QPushButton]

        self.addItem()

    def setupItems(self) -> None:
        n: int = len(self.itemWeights_ledits)

        # liczba value, weight, remove button sa ostosowywane (odpoweidnie ustawienie tychże i additemButton)
        # wartości są kolejno dodawane do value, weight

    def removeItem(self) -> None:
        id: int = self.removeitem_buttons.index(self.sender())

        # usunięcie itemu (value, weight, removeButton) o wskazanym id
        # przesunięcie niższych itemów i addItemButton w górę

    def addItem(self) -> None:
        self.itemValues_ledits.append(QLineEdit(self))
        self.itemValues_ledits[-1].setFixedSize(150, 40)
        self.itemValues_ledits[-1].move(75, 120 + 50 * len(self.itemValues_ledits))
        self.itemValues_ledits[-1].setText('0,0')
        self.itemValues_ledits[-1].setValidator(QDoubleValidator(0.0, sys.float_info.max, 16))
        self.itemValues_ledits[-1].textEdited.connect(self.valueEdited)
        self.itemValues_ledits[-1].show()

        self.itemWeights_ledits.append(QLineEdit(self))
        self.itemWeights_ledits[-1].setFixedSize(150, 40)
        self.itemWeights_ledits[-1].move(275, 120 + 50 * len(self.itemValues_ledits))
        self.itemWeights_ledits[-1].setText('0,0')
        self.itemWeights_ledits[-1].setValidator(QDoubleValidator(0.0, sys.float_info.max, 16))
        self.itemWeights_ledits[-1].textEdited.connect(self.weightEdited)
        self.itemWeights_ledits[-1].show()

        self.removeitem_buttons.append(QPushButton(self))
        self.removeitem_buttons[-1].setFixedSize(40, 40)
        self.removeitem_buttons[-1].move(450, 120 + 50 * len(self.removeitem_buttons))
        self.removeitem_buttons[-1].setText('-')
        self.removeitem_buttons[-1].clicked.connect(self.removeItem)
        self.removeitem_buttons[-1].show()

        self.items.append([0.0, 0.0])

        self.addItem_button.move(450, 170 + 50 * len(self.itemValues_ledits))

        # co jak nie ma miejsca

    def capacityEdited(self, text: str) -> None:
        self.capacity = float(text.replace(',', '.'))

    def valueEdited(self, text: str) -> None:
        id: int = self.itemValues_ledits.index(self.sender())
        self.items[id][0] = float(text.replace(',', '.'))

    def weightEdited(self, text: str) -> None:
        id: int = self.itemWeights_ledits.index(self.sender())
        self.items[id][1] = float(text.replace(',', '.'))

    def readFile(self) -> None:
        openFilePath: str = QFileDialog.getOpenFileName(self, 'Open File', './', '.json (*.json) ;; .* (*.*)')[0]

        if openFilePath:
            with open(openFilePath, 'r', encoding='utf-8') as file:
                data: dict = json.load(file)

                for v, w in data['items']:
                    if 0.0 > float(v):
                        print(f'Data contains item with negative value: ({v}, {w})', file=sys.stderr)
                        return

                    if 0.0 > float(w) or float(w) > float(data['capacity']):
                        print(
                            f'Data contains item with weigth that is either negative or grater than capacity: ({v}, {w})',
                            file=sys.stderr)
                        return

                self.capacity = data['capacity']
                self.items = data['items']

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
