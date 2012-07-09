#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QListWidgetItem
from ui.gen.mainWindow import Ui_MainWindow
from ui.gen.dashboard import Ui_Form as Ui_Form_Dashboard
from ui.gen.fitxa import Ui_Form as Ui_Form_Fitxa
from ui.gen.search_results import Ui_Form as Ui_Form_Search
from ui.gen.search_quick import Ui_Dialog as Ui_Dialog_Search
from collector.search import bgg
from tests import mocks

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class GameboardPersistence():

    items = mocks.items

    def getLast(self, count):
        result = self.items[:count]
        return result

    def get(self, title):
        for a in self.items:
            if title == a['title']:
                return a
        return {}


class Collection():

    def __init__(self):
        self.db = GameboardPersistence()

    def getLast(self):
        """ Finds last items created at the collection."""
        return self.db.getLast(10)
        #TODO this is a mock, make work over persistance class
        return [
                'Kolonisten van Catan: Europa Ontwaakt'
            ]

    def get(self, title):
        return self.db.get(title)


class Worker_Search(QtCore.QThread):

    searchComplete = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.results = {}

    def search(self, text):
        #log.debug('Searching...')
        self.action = 'search'
        self.params = {'query': text}
        self.start()

    def run(self):
        if self.action == 'search':
            p = bgg.search(self.params['query'], bgg.bgg_search_provider, bgg.bgg_search_filter)

            self.results['search'] = p
            self.searchComplete.emit()
            return
        if self.action == 'lastgames':
            self.results['lastgames'] = []
            return

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
        if str(args['query']) != '':
            self.search(str(args['query']))
        else:
            self.progressBar.hide()

    def search(self, text):
        self.bSearch.setDisabled(True)
        self.listWidget.clear()
        self.progressBar.show()
        self.worker.search(str(text))

    def searchComplete(self):
        self.bSearch.setEnabled(True)
        self.progressBar.hide()
        results = self.worker.getLastResult()
        for a in results['search']:
            item = QListWidgetItem(a[0])
            self.listWidget.addItem(item)
            del item


class Ui_Fitxa(QtGui.QWidget, Ui_Form_Fitxa):

    row = 0

    def __init__(self, item, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Fitxa, self).__init__(parent, flags)
        # TODO obtain full item, not only the title
        self.setupUi(item)

    def createLabel(self, text, label=False):
        item = QtGui.QLabel(self)
        if label:
            item.setFont(self.fontLabel)
        else:
            item.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        item.setText(text)
        item.setObjectName(_fromUtf8(text))
        return item

    def createField(self, label, text):
        columnspan = 1
        column = 0
        rowspan = 1
        #TODO add support for multiavalue fields
        itemLabel = self.createLabel(label, True)
        self.fieldsLayout.addWidget(itemLabel, self.row, column, rowspan, columnspan)
        column += 1
        if not isinstance(text, list):
            text = [text]
        for i in text:
            item = self.createLabel(i)
            self.fieldsLayout.addWidget(item, self.row, column, rowspan, columnspan)
            self.row += 1
        self.row += 1

    def setupUi(self, item):
        super(Ui_Fitxa, self).setupUi(self)
        obj = Collection().get(str(item.text()))
        self.lTitle.setText(item.text())
        self.fontLabel = QtGui.QFont()
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)
        self.createField('Title', obj['title'])
        self.createField('Designer/s', obj['designer'])
        self.createField('Artist/s', obj['artist'])
        self.bDashboard.connect(self.bDashboard, QtCore.SIGNAL(_fromUtf8("linkActivated(QString)")), lambda s: self.parent().viewDashboard())
        # TODO set image: we need to store it somewhere... but where is the best place?
        import os
        self.image.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), obj['image'])))

class Ui_Dashboard(QtGui.QWidget, Ui_Form_Dashboard):

    def __init__(self, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Dashboard, self).__init__(parent, flags)
        self.setupUi()

    def _show_fitxa(self, item):
        self.parent().viewFitxa(item)

    def setupUi(self):
        super(Ui_Dashboard, self).setupUi(self)
        self.loadLastGames(self.listWidget)
        self.bSearch.connect(self.bSearch, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda: self.parent().searchResults(self.lSearch.text()))

        self.listWidget.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem *)")), lambda s: self.parent().viewFitxa(s))

    def loadLastGames(self, listContainer):
        lastGames = Collection().getLast()
        for i in lastGames:
            item = QListWidgetItem(i['title'])
            listContainer.addItem(item)


class Ui_Application(QtGui.QMainWindow, Ui_MainWindow):

    fullscreen = False

    def switchFullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.showFullScreen()
        else:
            # TODO go to the previous mode!
            self.showNormal()

    def viewDashboard(self):
        dashboardWidget = Ui_Dashboard(self)
        self.setCentralWidget(dashboardWidget)

    def viewQuickSearch(self):
        dialog = QtGui.QDialog()
        ui = Ui_Dialog_Search()
        ui.setupUi(dialog)
        dialog.exec_()
        result = dialog.result()
        if result == 1:
            # Accepted
            self.searchResults(ui.lineEdit.text())
        #TODO obtain response of the dialog

    def searchResults(self, text):
        w = QtGui.QWidget()
        ui = Ui_Search()
        ui.setupUi(w, self, {'query': text})
        self.setCentralWidget(w)

    def viewFitxa(self, item):
        fitxaWidget = Ui_Fitxa(item, self)
        self.setCentralWidget(fitxaWidget)

    def setupUi(self):
        super(Ui_Application,  self).setupUi(self)
        self.viewDashboard()
        QtCore.QObject.connect(self.actionView_Dashboard, QtCore.SIGNAL(_fromUtf8("triggered()")), self.viewDashboard)
        QtCore.QObject.connect(self.actionQuick_search, QtCore.SIGNAL(_fromUtf8("triggered()")), self.viewQuickSearch)
        QtCore.QObject.connect(self.actionFullscreen, QtCore.SIGNAL(_fromUtf8("triggered()")), self.switchFullscreen)
        QtCore.QObject.connect(self.actionSearch_game, QtCore.SIGNAL(_fromUtf8("triggered()")), lambda: self.searchResults(''))
        #dashboard.setupUi(dashboardWidget, self.centralwidget)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Ui_Application()
    ui.setupUi()
    # Show window
    ui.show()
    # Bring window to front
    ui.raise_()
    sys.exit(app.exec_())
