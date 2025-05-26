import sys

from PyQt6.QtWidgets import QApplication

from generator.generatorApp import generatorApp


def main() -> None:
    app: QApplication = QApplication(sys.argv)
    # app.setStyle('Fusion')
    generator: generatorApp = generatorApp()
    generator.show()

    app.exec()


if __name__ == '__main__':
    main()
