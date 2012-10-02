# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.dashboard import Ui_Form
from ui.helpers.customtoolbar import CustomToolbar, Topbar
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
        self.settings = self.get_dashboard_settings()
        self.setupUi()

    def get_dashboard_settings(self):
        settings = {}
        collections = self.parent().collection.collections
        items = []
        for collection in collections.values():
            image = collection.get_image()
            if image is None:
                image = ":folder.png"
            items.append(
                {'class': 'link', 'name': collection.getName(),
                 'path': 'view/collection/collection/' + collection.name,
                 'image': image}
                )
        # TODO allow personalization of the new entry button?
        if len(collections) > 0:
            main_collection = collections.values()[0]
            settings['lastcollection'] = main_collection.name
            items.extend([
                {'class': 'spacer'},
                {'class': 'line'},
                {'class': 'link',
                 'name': str(self.tr('New <b>%s</b>')) % main_collection.getName(),
                 'path': 'view/add/collection/' + main_collection.name,
                 'image': ':/add.png'}
            ])
        else:
            settings['lastcollection'] = None

        settings['items'] = items
        return settings

    def setupUi(self):
        """Creates the ui elements for the dashboard.
        This function overrides the Ui_Form function creating thinks that
        aren't easy to do with the QT Designer"""
        super(Ui_Dashboard, self).setupUi(self)
        self.last_files(self.listWidget)
        self.bSearch.connect(
            self.bSearch,
            QtCore.SIGNAL(_fromUtf8("clicked()")),
            lambda: self.parent().display_view(
                'search',
                {'term': self.lSearch.text()}))

        Topbar(widget=self.topbar, icon=':ico/dashboard.png',
               title=self.tr("Dashboard").toUpper())
        self._loadToolbar()
        # TODO lastgames must be a widget and will ofer a way to choose
        #  the collection to display and the title
        self.listWidget.connect(
            self.listWidget,
            QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem *)")),
            lambda s: self.parent().display_view(
                'fitxa',
                {'item': s.id, 'collection': 'boardgames'}))

    def _loadToolbar(self):
        """ Creates the toolbar for the view, this function must be
         called after the Ui_Form.setupUi has been called."""
        items = self.settings['items']
        CustomToolbar(self.toolbar, items, self._toolbarCallback)

    def _toolbarCallback(self, uri):
        self.parent().collector_uri_call(uri)

    def last_files(self, listContainer):
        collection_id = self.settings['lastcollection']
        if collection_id is not None:
            collection = self.parent().collection.getCollection(collection_id)
            label = collection.getName()
            self.lLastItems.setText(str(self.tr("Last %s")) % label)
            lastObjects = collection.getLast()
            for i in lastObjects:
                text = i[collection.schema.default]
                item = FitxaListItem(i['id'], text != '' and text or str(self.tr('Entry %d')) % i['id'] )
                listContainer.addItem(item)
        else:
            self.lLastItems.setText(self.tr("Warning: No collection available!"))


class DashboardView():

    def __init__(self, parent):
        self.parent = parent

    def run(self, params={}):
        self.parent.fitxa = None
        dashboardWidget = Ui_Dashboard(self.parent)
        self.parent.setCentralWidget(dashboardWidget)
