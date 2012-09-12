# -*- coding: utf-8 -*-

# This is only needed for Python v2 but is harmless for Python v3.
from PyQt4 import QtCore
from PyQt4.QtGui import QWidget
from ui.gen.search_results import Ui_Form
from ui.workers.search import Worker_Search
from ui.helpers.customtoolbar import Topbar
from ui.helpers.items import FitxaListItem
from ui.widgetprovider import WidgetProvider


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_Search(QWidget, Ui_Form):

    worker = None

    def __init__(self, query, parent, flags=None):
        """ Creates a new search view"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Search, self).__init__(parent, flags)
        self.setupUi(query)

    def setupUi(self, query):
        super(Ui_Search, self).setupUi(self)
        Topbar(widget=self.topbar, icon=':ico/search.png',
               title='SEARCH')
        if query:
            self.lSearch.setText(query)
        self.bSearch.connect(
            self.bSearch,
            QtCore.SIGNAL(_fromUtf8("clicked()")),
            lambda: self.search(self.lSearch.text()))
        self.listWidget.connect(
            self.listWidget,
            QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem *)")),
            self.itemSelected)
        self.worker = Worker_Search()
        self.worker.searchComplete.connect(lambda: self.searchComplete())
        if str(query) != '':
            self.search(str(query))
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
            item = FitxaListItem(a['id'], a['name'])
            self.listWidget.addItem(item)
            del item
        # TODO display error message if nothing was fount or an error hapenned
        # self.parent().viewInfo('Hola!')

    def searchCompletePlugin(self):
        # TODO update and change QListWidgetItem for pluginFitxaItem
        self.bSearch.setEnabled(True)
        self.progressBar.hide()
        results = self.worker.getLastResult()
        for a in results['searchPlugins']:
            item = QListWidgetItem(a[0])
            self.listWidget.addItem(item)
            del item

        # TODO display error message if nothing was fount or an error hapenned
        # self.parent().viewInfo('Hola!')

    def itemSelected(self, listItem):
        self.parent().displayView(
            'fitxa',
            {'item': listItem.id, 'collection': 'boardgames'}
        )


class SearchView(WidgetProvider):

    def getWidget(self, params):
        term = params['term']
        widget = Ui_Search(term, self.parent)
        return widget
