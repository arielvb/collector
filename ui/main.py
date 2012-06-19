# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from gen.mainWindow import Ui_MainWindow
from gen.dashboard import Ui_Form


class Ui_Application(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super(Ui_Application,  self).setupUi(MainWindow)
        Ui_Form().setupUi(self.wContainer)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_Application()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # Bring window to front
    MainWindow.raise_()
    sys.exit(app.exec_())
