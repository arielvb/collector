# -*- coding: utf-8 -*-

# This is only needed for Python v2 but is harmless for Python v3.
from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QApplication, QMessageBox, QDialog
from ui.gen.search_results import Ui_Form
from ui.workers.search import Worker_Search, Worker_Discover, STATUS_OK
from ui.gen.search_quick import Ui_Dialog as Ui_Dialog_Search
from ui.helpers.customtoolbar import Topbar
from ui.helpers.items import FitxaListItem
from ui.widgetprovider import WidgetProvider


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_Search(QWidget, Ui_Form):

    # TODO don't call worker directly, move to parent and this will
    #  define wich workers must exit when a view is being destroyed
    worker = Worker_Search()
    title = QApplication.translate("Form", "Search",
                                   None, QApplication.UnicodeUTF8)
    description = None

    def __init__(self, query, parent, flags=None):
        """ Creates a new search view"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Search, self).__init__(parent, flags)
        self.setupUi(query)

    def setupUi(self, query):
        super(Ui_Search, self).setupUi(self)

        Topbar(widget=self.topbar, icon=':ico/search.png',
               title=self.title.toUpper(), description=self.description)
        if query:
            self.lSearch.setText(_fromUtf8(query))
        self.bSearch.connect(
            self.bSearch,
            QtCore.SIGNAL(_fromUtf8("clicked()")),
            lambda: self.search(self.lSearch.text()))
        self.listWidget.connect(
            self.listWidget,
            QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem *)")),
            self.itemSelected)

        self.worker.searchComplete.connect(lambda r: self.searchComplete(r))
        if isinstance(query, QtCore.QString):
            query = query.toUtf8()
        if query != u'':
            self.search(str(query))
        else:
            self.progressBar.hide()

    def search(self, text):
        self.bSearch.setDisabled(True)
        self.listWidget.clear()
        self.progressBar.show()
        self.query = text
        if isinstance(text, QtCore.QString):
            text = text.toUtf8()
        self.worker.search(str(text))

    def searchComplete(self, results):
        self.bSearch.setEnabled(True)
        self.progressBar.hide()
        if results.status != STATUS_OK:
            QMessageBox.warning(
                self.tr("Ooops!\nSomething happened and the search" +
                        "could'nt be completed."))
            return
        for result in results.results:
            item = FitxaListItem(result['id'], result['name'])
            self.listWidget.addItem(item)
            del item

    def itemSelected(self, listItem):
        self.parent().displayView(
            'fitxa',
            {'item': listItem.id, 'collection': 'boardgames'}
        )


class Ui_SearchPlugin(Ui_Search):

    title = QApplication.translate("Form", "Discover",
                                   None, QApplication.UnicodeUTF8)
    description = ("Discover allows you find new objects for your collection,"
                  " type somenthing in the searchbox and the plugins"
                  " will do the hardwork.")
    worker = Worker_Discover()

    def searchComplete(self, results):
        self.bSearch.setEnabled(True)
        self.progressBar.hide()
        if results.status != STATUS_OK:
            # TODO parse errors
            QMessageBox.warning(
                self,
                self.tr("Warning"),
                self.tr("Ooops!\nSomething happened and the search" +
                        "could'nt be completed."))
            return
        self.results = results.results
        for result in results.results:
            item = FitxaListItem(1, result[0])
            self.listWidget.addItem(item)
            del item

    def itemSelected(self, listItem):
        self.parent().displayView(
            'fitxa',
            {
                'item': listItem.id,
                'collection': 'plugin:PluginBoardgamegeek',
                'referer': {
                    'view': 'discover',
                    'params': {'term': self.query, 'results': self.results}
                    }
            }
        )


class DiscoverView(WidgetProvider):

    def getWidget(self, params):
        term = ''
        if 'term' in params:
            term = params['term']
        widget = Ui_SearchPlugin(term, self.parent)
        return widget


class SearchView(WidgetProvider):

    def getWidget(self, params):
        term = ''
        if 'term' in params:
            term = params['term']
        widget = Ui_Search(term, self.parent)
        return widget


class SearchDialog(WidgetProvider):

        mode = WidgetProvider.DIALOG_WIDGET

        def getWidget(self, params):
            dialog = QDialog(self.parent)
            self.ui = Ui_Dialog_Search()
            self.ui.setupUi(dialog)
            return dialog

        def after_exec(self, widget):
            result = widget.result()
            if result == 1:
                # Accepted
                self.parent.displayView(
                    'search',
                    {'term': self.ui.lineEdit.text().toUtf8()})
