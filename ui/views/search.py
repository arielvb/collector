# -*- coding: utf-8 -*-
"""
Search
------

Search related views: item search, quick search and discover.

"""
# This is only needed for Python v2 but is harmless for Python v3.
from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QApplication, QMessageBox, QDialog
from ui.gen.search_results import Ui_Form, _fromUtf8
from ui.workers.search import Worker_Search, Worker_Discover, STATUS_OK
from ui.gen.search_quick import Ui_Dialog as Ui_Dialog_Search
from ui.helpers.customtoolbar import Topbar
from ui.helpers.items import ObjectListItem, FitxaListItem
from ui.widgetprovider import WidgetProvider


class Ui_Search(QWidget, Ui_Form):

    # TODO don't call worker directly, move to parent and this will
    #  define wich workers must exit when a view is being destroyed
    worker = Worker_Search()
    title = QApplication.translate("Form", "Search",
                                   None, QApplication.UnicodeUTF8)
    description = None

    def __init__(self, query, results, parent, flags=None):
        """ Creates a new search view"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Search, self).__init__(parent, flags)
        self.results = []
        self.query = query
        if results is None:
            results = []
        self.setupUi(query, results)

    def setupUi(self, query, results):
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
            QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem *)")),
            self.itemSelected)

        self.worker.searchComplete.connect(lambda r: self.searchComplete(r))
        if isinstance(query, QtCore.QString):
            query = query.toUtf8()
        if query != u'' and len(results) == 0:
            self.search(str(query))
        else:
            self.progressBar.hide()
            if len(results) > 0:
                self.addResults(results)

    def search(self, text):
        self.bSearch.setDisabled(True)
        self.listWidget.clear()
        self.progressBar.show()
        self.query = text
        self.parent().statusBar().showMessage(self.tr('Searching...'))
        if isinstance(text, QtCore.QString):
            text = text.toUtf8()
        self.worker.search(str(text))

    def searchComplete(self, results):
        """Process the results of a search, *results* must be instance of
         WorkerResult"""
        self.parent().statusBar().clearMessage()
        self.bSearch.setEnabled(True)
        self.progressBar.hide()

        if results.status != STATUS_OK:
            QMessageBox.warning(self,
                self.tr("Collector"),
                self.tr("Ooops!\nSomething happened and the search" +
                        " could'nt be completed."))
        else:
            self.addResults(results.results)

    def addResults(self, listResults):
        """Adds the each elelemt of listResults to the results list widget"""
        for result in listResults:
            item = FitxaListItem(result['id'], result['title'])
            self.listWidget.addItem(item)
            del item
        self.results.extend(listResults)

    def itemSelected(self, listItem):
        self.worker.searchComplete.disconnect()
        self.parent().display_view(
            'fitxa',
            {'item': listItem.id, 'collection': 'boardgames'}
        )


class Ui_Discover(Ui_Search):

    title = QApplication.translate("Ui_Discover", "Discover",
                                   None, QApplication.UnicodeUTF8)
    description = QApplication.translate("Ui_Discover",
        "Discover allows you find new objects for your collection,"
        " type something in the searchbox and the plugins"
        " will do the hardwork.", None, QApplication.UnicodeUTF8)

    worker = Worker_Discover()

    def addResults(self, results):
        """Overrides the default addResults because the results from plugins
         are a little bit different"""
        # TODO the results of a plugin must be in the same format of the search
        for result in results:
            item = ObjectListItem(result, result['name'])
            self.listWidget.addItem(item)
            del item
        self.results.extend(results)

    def itemSelected(self, listItem):
        self.worker.searchComplete.disconnect()
        self.parent().display_view(
            'pluginfile',
            {
                'id': listItem.obj['id'],
                'plugin': listItem.obj['plugin'],
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
        results = None
        if 'results' in params:
            results = params['results']
        widget = Ui_Discover(term, results, self.parent)
        return widget


class SearchView(WidgetProvider):

    def getWidget(self, params):
        term = ''
        if 'term' in params:
            term = params['term']
        results = None
        if 'results' in params:
            results = params['results']
        widget = Ui_Search(term, results, self.parent)
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
                self.parent.display_view(
                    'search',
                    {'term': self.ui.lineEdit.text().toUtf8()})
