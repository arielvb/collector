# -*- coding: utf-8 -*-
# pylint: disable-msg=C0103,E1101
"""
Search
------

Search related views: item search, quick search and discover.

"""
from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QApplication, QMessageBox, QDialog
from ui.gen.search_results import Ui_Form, _fromUtf8
from ui.workers.search import Worker_Search, Worker_Discover, STATUS_OK
from ui.gen.search_quick import Ui_Dialog as Ui_Dialog_Search
from ui.helpers.customtoolbar import Topbar, CustomToolbar
from ui.helpers.items import ObjectListItem, FitxaListItem
from ui.widgetprovider import WidgetProvider
from engine.controller import Collector


class Ui_Search(QWidget, Ui_Form):
    """Search widget"""

    # TODO don't call worker directly, move to parent and this will
    #  define wich workers must exit when a view is being destroyed
    worker = Worker_Search()
    title = QApplication.translate("Form", "Search",
                                   None, QApplication.UnicodeUTF8)
    icon = ":ico/search.png"

    description = None

    def __init__(self, query, results, parent, collection=None, flags=None):
        """ Creates a new search view"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Search, self).__init__(parent, flags)
        self.results = []
        self.collection = None
        collections = Collector.get_instance().get_manager('collection')
        if collection is not None:
            self.collection = collections.get_collection(collection)
            self.pretty = self.collection.schema.default
        self.query = query
        if results is None:
            results = []
        self.setupUi(query, results)

    def setupUi(self, query, results):
        super(Ui_Search, self).setupUi(self)

        Topbar(widget=self.topbar, icon=self.icon,
               title=self.title.toUpper(), description=self.description)

        # Toolbar
        items = [
            {'class':'link', 'name': self.tr('Dashboard'),
             'path': 'view/dashboard', 'image': ':/dashboard.png'},
            {'class': 'spacer'}
        ]
        CustomToolbar(self.toolbar, items, self.parent().collector_uri_call)

        if query:
            self.lSearch.setText(_fromUtf8(query))
        self.connect(
            self.bSearch,
            QtCore.SIGNAL(_fromUtf8("clicked()")),
            lambda: self.search(self.lSearch.text()))
        self.listWidget.connect(
            self.listWidget,
            QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem *)")),
            self.item_selected)

        self.worker.searchComplete.connect(self.searchComplete)
        if isinstance(query, QtCore.QString):
            query = query.toUtf8()
        if query != u'' and len(results) == 0:
            self.search(str(query))
        else:
            self.progressBar.hide()
            if len(results) > 0:
                self.addResults(results)

    def search(self, text):
        """Search slot"""
        self.bSearch.setDisabled(True)
        self.listWidget.clear()
        self.progressBar.show()
        self.query = text
        self.parent().statusBar().showMessage(self.tr('Searching...'))
        if isinstance(text, QtCore.QString):
            text = text.toUtf8()
            self.query = text
        self.worker.search({'like': [self.pretty, unicode(text, 'utf-8')]},
                           self.collection.get_id())

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
            # TODO partial results support
            self.results = []
            self.addResults(results.results)

    def addResults(self, listResults):
        """Adds the each elelemt of listResults to the results list widget"""

        for result in listResults:
            item = FitxaListItem(result['id'], result[self.pretty])
            self.listWidget.addItem(item)
            del item
        self.results.extend(listResults)

    def item_selected(self, listItem):
        "item selected"
        self.worker.searchComplete.disconnect()
        self.parent().display_view(
            'fitxa',
            {'item': listItem.id, 'collection': 'boardgames'}
        )


class Ui_Discover(Ui_Search):
    """Discover widget"""

    title = QApplication.translate("Ui_Discover", "Discover",
                                   None, QApplication.UnicodeUTF8)
    description = QApplication.translate("Ui_Discover",
        "Discover allows you find new objects for your collection,"
        " type something in the searchbox and the plugins"
        " will do the hardwork.", None, QApplication.UnicodeUTF8)

    icon = ":ico/browser.png"

    worker = Worker_Discover()

    def search(self, text):
        """Search slot"""
        self.bSearch.setDisabled(True)
        self.listWidget.clear()
        self.progressBar.show()
        self.query = text
        self.parent().statusBar().showMessage(self.tr('Searching...'))
        if isinstance(text, QtCore.QString):
            text = text.toUtf8()
            self.query = text
        self.worker.search(unicode(text, 'utf-8'))

    def addResults(self, results):
        """Overrides the default addResults because the results from plugins
         are a little bit different"""
        # TODO the results of a plugin must be in the same format of the search
        for result in results:
            item = ObjectListItem(result, result['name'])
            self.listWidget.addItem(item)
            del item
        self.results.extend(results)

    def item_selected(self, listItem):
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
    """Discover view"""

    def get_widget(self, params):
        term = ''
        if 'term' in params:
            term = params['term']
        results = None
        if 'results' in params:
            results = params['results']
        widget = Ui_Discover(term, results, self.parent)
        return widget


class SearchView(WidgetProvider):
    """Quick search view"""

    def get_widget(self, params):
        term = params.get('term', '')
        results = params.get('results', None)
        collection = params.get('collection', None)
        if collection == None:
            raise ValueError()
        widget = Ui_Search(term, results, self.parent, collection)
        return widget


class SearchDialog(WidgetProvider):
    """Quick Search dialog view"""

    mode = WidgetProvider.DIALOG_WIDGET
    dialog = None
    collection = None

    def get_widget(self, params):
        dialog = QDialog(self.parent)
        self.dialog = Ui_Dialog_Search()
        # FIXME collection must be loaded from settings
        self.collection = 'boardgames'
        self.dialog.setupUi(dialog)
        return dialog

    def after_exec(self, widget):
        result = widget.result()
        if result == 1:
            # Accepted
            self.parent.display_view(
                'search',
                {
                 'term': self.dialog.lineEdit.text().toUtf8(),
                 'collection': self.collection
                })
