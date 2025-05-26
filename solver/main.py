import sys
from solver.solverApp import solverApp
from PyQt6.QtWidgets import QApplication


def main() -> None:
    app : QApplication = QApplication(sys.argv)
    app.setStyle('Fusion')
    solver : solverApp = solverApp()
    solver.show()

    app.exec()


if __name__ == '__main__':
    main()
