import sys

from PyQt6.QtGui import QPalette, QColor

from generator.generatorApp import generatorApp
from PyQt6.QtWidgets import QApplication


def main() -> None:
    app : QApplication = QApplication(sys.argv)
    # app.setStyle('Fusion')
    generator : generatorApp = generatorApp()
    generator.show()

    app.exec()


if __name__ == '__main__':
    main()
