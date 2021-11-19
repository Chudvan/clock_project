# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import mainwindow

import sys
from PyQt5.QtWidgets import QApplication

import clock


# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    app = QApplication(sys.argv)

    w = mainwindow.Ui_MainWindow()
    w.show()
    sys.exit(app.exec_())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
