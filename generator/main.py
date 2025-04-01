import sys
from generator.generatorApp import generatorApp
from PyQt6.QtWidgets import QApplication


def main():
    app : QApplication = QApplication(sys.argv)
    generator : generatorApp = generatorApp()
    generator.show()

    app.exec()


if __name__ == '__main__':
    main()
