# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QListWidgetItem
from ui.gen.dashboard import Ui_Form
from ui.helpers.customtoolbar import CustomToolbar
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class FitxaList(QListWidgetItem):

    def __init__(self, id, text):
        super(FitxaList, self).__init__(text)
        self.id = id


# TODO store settings in a config file
dashboard_settings = {

    'items': [
            {'class':'link', 'name': 'Boardgames', 'path': 'collection/boardgames', 'image': ':/boards.png'},
            {'class':'link', 'name': 'Authors & Designers', 'path': 'collection/people', 'image': ':/author.png'},
            {'class': 'spacer'},
            {'class': 'line'},
            {'class':'link', 'name': 'New <b>Boardgame</b>', 'path': 'collection/boardgames/add', 'image': ':/add.png'},
        ],

    'lastcollection': 'boardgames'
}


class Ui_Dashboard(QtGui.QWidget, Ui_Form):

    def __init__(self, parent=None, flags=None):
        """ Creates a new dashboard view"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Dashboard, self).__init__(parent, flags)
        global dashboard_settings
        self.settings = dashboard_settings
        self.setupUi()

    def setupUi(self):
        """Creates the ui elements for the dashboard.
        This function overrides the Ui_Form function creating thinks that aren't easy to do with the QT Designer"""
        super(Ui_Dashboard, self).setupUi(self)
        self.loadLastGames(self.listWidget)
        self.bSearch.connect(self.bSearch,
            QtCore.SIGNAL(_fromUtf8("clicked()")),
            lambda: self.parent().searchResults(self.lSearch.text()))
        self._loadToolbar()
        # TODO lastgames must be a widget and will ofer a way to choose the collection to display and the title
        self.listWidget.connect(self.listWidget,
            QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem *)")),
            lambda s: self.parent().displayView('fitxa', {'item': s.id, 'collection': 'boardgames'}))

    def _loadToolbar(self):
        """ Creates the toolbar for the view, this function must be called after the Ui_Form.setupUi has been called."""
        items = self.settings['items']
        CustomToolbar(self.toolbar, items, self._toolbarCallback)

    def _toolbarCallback(self, uri):
        # TODO make more generic without if, else maybe a collector uri scheme class
        # TODO parse arguments
        params_encoded = uri.split('/')
        # delete first params, because is the view name
        #del params_encoded[0]
        params = {}
        key = None
        for a in params_encoded:
            if key is None:
                key = a
            else:
                params[str(key)] = str(a)
                key = None
        if uri == 'collector:collection/boardgames':
            self.parent().displayView('collection', params)
            pass
        elif uri == 'collector:collection/people':
            self.parent().displayView('collection', params)
            pass
        elif uri == 'collector:collection/boardgames/add':
            pass

    def loadLastGames(self, listContainer):
        collection = self.parent().collection.getCollection(self.settings['lastcollection'])
        label = collection.getName()
        self.lLastItems.setText("Last %s" % label)
        lastObjects = collection.getLast10()
        for i in lastObjects:
            item = FitxaList(i['id'], i['name'])
            listContainer.addItem(item)


class DashboardView():

    def __init__(self, parent):
        self.parent = parent

    def run(self, params={}):
        self.parent.fitxa = None
        dashboardWidget = Ui_Dashboard(self.parent)
        self.parent.setCentralWidget(dashboardWidget)
