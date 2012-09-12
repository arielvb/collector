# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.dashboard import Ui_Form
from ui.helpers.customtoolbar import CustomToolbar
from ui.helpers.items import FitxaListItem

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


# TODO store settings in a config file
dashboard_settings = {

    'items': [
        {'class':'link', 'name': 'Boardgames',
         'path': 'view/collection/collection/boardgames',
         'image': ':/boards.png'},
        {'class':'link', 'name': 'Authors & Designers',
         'path': 'view/collection/collection/people',
         'image': ':/author.png'},
        {'class': 'spacer'},
        {'class': 'line'},
        {'class': 'link', 'name': 'New <b>Boardgame</b>',
         'path': 'view/add/collection/boardgames', 'image': ':/add.png'},
    ],

    'lastcollection': 'boardgames',
}


class Ui_Dashboard(QtGui.QWidget, Ui_Form):

    def __init__(self, parent, flags=None):
        """ Creates a new dashboard view"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Dashboard, self).__init__(parent, flags)
        global dashboard_settings
        self.settings = dashboard_settings
        self.setupUi()

    def setupUi(self):
        """Creates the ui elements for the dashboard.
        This function overrides the Ui_Form function creating thinks that
        aren't easy to do with the QT Designer"""
        super(Ui_Dashboard, self).setupUi(self)
        self.loadLastGames(self.listWidget)
        self.bSearch.connect(
            self.bSearch,
            QtCore.SIGNAL(_fromUtf8("clicked()")),
            lambda: self.parent().displayView(
                'search',
                {'term': self.lSearch.text()}))
        self._loadToolbar()
        # TODO lastgames must be a widget and will ofer a way to choose
        #  the collection to display and the title
        self.listWidget.connect(
            self.listWidget,
            QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem *)")),
            lambda s: self.parent().displayView(
                'fitxa',
                {'item': s.id, 'collection': 'boardgames'}))

    def _loadToolbar(self):
        """ Creates the toolbar for the view, this function must be
         called after the Ui_Form.setupUi has been called."""
        items = self.settings['items']
        CustomToolbar(self.toolbar, items, self._toolbarCallback)

    def _toolbarCallback(self, uri):
        # TODO make more generic without if,
        #  else maybe a collector uri scheme class
        # TODO parse arguments
        self.parent().collectorURICaller(uri)

    def loadLastGames(self, listContainer):
        collection = self.parent().collection.getCollection(
            self.settings['lastcollection'])
        label = collection.getName()
        self.lLastItems.setText("Last %s" % label)
        lastObjects = collection.getLast10()
        for i in lastObjects:
            item = FitxaListItem(i['id'], i['name'])
            listContainer.addItem(item)


class DashboardView():

    def __init__(self, parent):
        self.parent = parent

    def run(self, params={}):
        self.parent.fitxa = None
        dashboardWidget = Ui_Dashboard(self.parent)
        self.parent.setCentralWidget(dashboardWidget)
