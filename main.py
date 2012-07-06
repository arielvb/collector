# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QListWidgetItem
from ui.gen.mainWindow import Ui_MainWindow
from ui.gen.dashboard import Ui_Form as Ui_Form_Dashboard
from ui.gen.fitxa import Ui_Form as Ui_Form_Fitxa
from ui.gen.search_results import Ui_Form as Ui_Form_Search
from ui.gen.search_quick import Ui_Dialog as Ui_Dialog_Search
from collector.search import bgg

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Worker_Search(QtCore.QThread):

    searchComplete = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.results = None

    def search(self, text):
        #log.debug('Searching...')
        self.action = 'search'
        self.params = {'query': text}
        self.start()

    def run(self):
        if self.action == 'search':
            self.results = bgg.search(self.params['query'], bgg.bgg_search_provider, bgg.bgg_search_filter)
            self.searchComplete.emit()

    def getLastResult(self):
        return self.results

    def __del__(self):
        self.wait()


class Ui_Search(Ui_Form_Search):

    worker = None

    def setupUi(self, container, window, args):
        super(Ui_Search, self).setupUi(container)
        if 'query' in args:
            self.lSearch.setText(args['query'])
        self.bSearch.connect(self.bSearch, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda: self.search(self.lSearch.text()))

        self.worker = Worker_Search()
        self.worker.searchComplete.connect(lambda: self.searchComplete())
        self.search(str(args['query']))

    def search(self, text):
        self.bSearch.setDisabled(True)
        self.listWidget.clear()
        self.progressBar.show()
        self.worker.search(str(text))

    def searchComplete(self):
        self.bSearch.setEnabled(True)
        self.progressBar.hide()
        results = self.worker.getLastResult()
        for a in results:
            item = QListWidgetItem(a[0])
            self.listWidget.addItem(item)
            del item


class Ui_Fitxa(Ui_Form_Fitxa):

    def setupUi(self, container, window):
        super(Ui_Fitxa, self).setupUi(container)
        self.bDashboard.connect(self.bDashboard, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda: window.viewDashboard())


class Ui_Dashboard(QtGui.QWidget, Ui_Form_Dashboard):

    window = None

    def __init__(self, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Dashboard, self).__init__(parent, flags)

    def _show_fitxa(self, item):
        self.window.viewFitxa()
        # self.windo.repaint()

    def setupUi(self, window):
        self.window = window
        super(Ui_Dashboard, self).setupUi(self)
        self.loadLastGames(self.listWidget)
        self.bSearch.connect(self.bSearch, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda: window.searchResults(self.lSearch.text()))

        self.listWidget.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem *)")), lambda s: self._show_fitxa(s))

    def loadLastGames(self, listContainer):
        lastGames = ['The Pillars of the Earth']
        for i in lastGames:
            item = QListWidgetItem(i)
            listContainer.addItem(item)


class Ui_Application(Ui_MainWindow):

    window = None
    fullscreen = False

    def switchFullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.window.showFullScreen()
        else:
            # TODO go to the previous mode!
            self.window.showNormal()

    def viewDashboard(self):
        #dashboardWidget = QtGui.QWidget()
        #Ui_Dashboard().setupUi(dashboardWidget, self)
        dashboardWidget = Ui_Dashboard()
        dashboardWidget.setupUi(self)
        self.window.setCentralWidget(dashboardWidget)

    def viewQuickSearch(self):
        Dialog = QtGui.QDialog()
        ui = Ui_Dialog_Search()
        ui.setupUi(Dialog)
        Dialog.exec_()
        #TODO obtain response of the dialog

    def searchResults(self, text):
        w = QtGui.QWidget()
        ui = Ui_Search()
        ui.setupUi(w, self, {'query': text})
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
        QtCore.QObject.connect(self.actionFullscreen, QtCore.SIGNAL(_fromUtf8("triggered()")), self.switchFullscreen)

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
