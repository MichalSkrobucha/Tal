import sys

from PyQt6.QtWidgets import QApplication

from solver.solverApp import solverApp


def main() -> None:
    app: QApplication = QApplication(sys.argv)
    app.setStyle('Fusion')
    solver: solverApp = solverApp()
    solver.show()

    app.exec()


if __name__ == '__main__':
    main()
