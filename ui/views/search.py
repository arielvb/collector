# -*- coding: utf-8 -*-

# This is only needed for Python v2 but is harmless for Python v3.
from PyQt4 import QtCore
from PyQt4.QtGui import QListWidgetItem
from ui.gen.search_results import Ui_Form
from ui.workers.search import Worker_Search
from ui.helpers.customtoolbar import Topbar


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_Search(Ui_Form):

    worker = None

    def setupUi(self, container, window, args):
        self.parent = lambda: window
        super(Ui_Search, self).setupUi(container)
        Topbar(widget=self.topbar, icon='search.png',
            title='SEARCH')
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
        # TODO display error message if nothing was fount or an error hapenned
        # self.parent().viewInfo('Hola!')
