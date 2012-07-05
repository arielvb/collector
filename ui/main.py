# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QListWidgetItem
from gen.mainWindow import Ui_MainWindow
from gen.dashboard import Ui_Form as Ui_Form_Dashboard
from gen.fitxa import Ui_Form as Ui_Form_Fitxa
from gen.search_results import Ui_Form as Ui_Form_Search
from gen.search_quick import Ui_Dialog as Ui_Dialog_Search

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_Search(Ui_Form_Search):

    def setupUi(self, container, window, args):
        super(Ui_Search, self).setupUi(container)
        if 'query' in args:
            self.lSearch.setText(args['query'])


class Ui_Fitxa(Ui_Form_Fitxa):

    def setupUi(self, container, window):
        super(Ui_Fitxa, self).setupUi(container)
        self.bDashboard.connect(self.bDashboard, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda: window.viewDashboard())


class Ui_Dashboard(Ui_Form_Dashboard):

    window = None

    def _show_fitxa(self, item):
        self.window.viewFitxa()
        # self.windo.repaint()

    def setupUi(self, container, window):
        self.window = window
        super(Ui_Dashboard, self).setupUi(container)
        self.loadLastGames(self.listWidget)
        self.bSearch.connect(self.bSearch, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda: window.searchResults(self.lSearch.text()))

        self.listWidget.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem *)")), lambda s: self._show_fitxa(s))
        #QtCore.QMetaObject.connectSlotsByName(container)

    def loadLastGames(self, listContainer):
        lastGames = ['The Pillars of the Earth']
        for i in lastGames:
            item = QListWidgetItem(i)
            listContainer.addItem(item)


class Ui_Application(Ui_MainWindow):

    window = None

    def viewDashboard(self):
        dashboardWidget = QtGui.QWidget()
        Ui_Dashboard().setupUi(dashboardWidget, self)
        self.window.setCentralWidget(dashboardWidget)

    def viewQuickSearch(self):
        Dialog = QtGui.QDialog()
        ui = Ui_Dialog_Search()
        ui.setupUi(Dialog)
        Dialog.exec_()


    def searchResults(self, text):
        w = QtGui.QWidget()
        Ui_Search().setupUi(w, self, {'query': text})
        self.window.setCentralWidget(w)

    def viewFitxa(self):
        fitxaWidget = QtGui.QWidget()
        Ui_Fitxa().setupUi(fitxaWidget, self)
        self.window.setCentralWidget(fitxaWidget)

    def setupUi(self, window):
        super(Ui_Application,  self).setupUi(window)
        self.window = window
        self.viewDashboard()
        QtCore.QObject.connect(self.actionView_Dashboard, QtCore.SIGNAL(_fromUtf8("triggered()")), self.viewDashboard)
        QtCore.QObject.connect(self.actionQuick_search, QtCore.SIGNAL(_fromUtf8("triggered()")), self.viewQuickSearch)

        #dashboard.setupUi(dashboardWidget, self.centralwidget)


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
