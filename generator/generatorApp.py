import json
import sys

from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog

class generatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.capacity: float = 0.0
        self.items: list[list[float, float]] = []  # [value, weight]

        self.readFile_button: QPushButton
        self.saveFile_button: QPushButton
        self.backpackCapacity_label: QLabel
        self.backpackCapacity_ledit: QLineEdit
        self.itemValue_label: QLabel
        self.itemValues_ledits: list[QLineEdit]
        self.itemWeight_label: QLabel
        self.itemWeights_ledits: list[QLineEdit]

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('Generator')
        self.setFixedSize(500, 500)
        self.move(710, 270)

        self.readFile_button = QPushButton(self)
        self.readFile_button.setFixedSize(150, 50)
        self.readFile_button.move(75, 50)
        self.readFile_button.setText('Read from file')
        self.readFile_button.clicked.connect(self.readFile)
        self.readFile_button.show()

        self.saveFile_button = QPushButton(self)
        self.saveFile_button.setFixedSize(150, 50)
        self.saveFile_button.move(275, 50)
        self.saveFile_button.setText('Save to file')
        self.saveFile_button.clicked.connect(self.saveFile)
        self.saveFile_button.setEnabled(False)
        self.saveFile_button.show()

        self.backpackCapacity_label = QLabel(self)
        self.backpackCapacity_label.setFixedSize(150, 50)
        self.backpackCapacity_label.move(75, 125)
        self.backpackCapacity_label.setText('Backpack capacity: ')
        self.backpackCapacity_label.show()

        self.backpackCapacity_ledit = QLineEdit(self)
        self.backpackCapacity_ledit.setFixedSize(150, 50)
        self.backpackCapacity_ledit.move(275, 125)
        self.backpackCapacity_ledit.setText('0')
        self.backpackCapacity_ledit.show()

        self.itemValue_label = QLabel(self)
        self.itemValue_label.setFixedSize(150, 50)
        self.itemValue_label.move(75, 200)
        self.itemValue_label.setText('Item Value:')
        self.itemValue_label.show()

        self.itemWeight_label = QLabel(self)
        self.itemWeight_label.setFixedSize(150, 50)
        self.itemWeight_label.move(275, 200)
        self.itemWeight_label.setText('Item Weight:')
        self.itemWeight_label.show()

        self.itemValues_ledits: list[QLineEdit]
        self.itemWeights_ledits: list[QLineEdit]

    def readFile(self) -> None:
        openFilePath: str = QFileDialog.getOpenFileName(self, 'Open File', './', '.json (*.json) ;; .* (*.*)')[0]

        if openFilePath:
            with open(openFilePath, 'r', encoding='utf-8') as file:
                data: dict = json.load(file)
                self.capacity = data['capacity']
                self.items = data['items']
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
