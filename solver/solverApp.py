from PyQt6.QtWidgets import QMainWindow


class solverApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle('Solver')
        self.setFixedSize(600, 600)
        self.move(660, 220)
