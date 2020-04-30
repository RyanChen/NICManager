from PyQt5 import QtWidgets
from main_form import MainUi

import sys

if __name__ == '__main__':
    def run_app():
        app = QtWidgets.QApplication(sys.argv)
        window = MainUi()
        window.show()
        app.exec_()
    run_app()
