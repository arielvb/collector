# -*- coding: utf-8 -*-
# pylint: disable-msg=C0103,E1101
# C0103:

from PyQt4 import QtCore, QtGui
from collector.ui.gen.dashboard import Ui_Form, _fromUtf8
from collector.ui.helpers.customtoolbar import CustomToolbar, Topbar
from collector.ui.helpers.items import FitxaListItem
from collector.ui.views import Page


class Ui_Dashboard(QtGui.QWidget, Ui_Form):
    """The dashboard widget"""

    def __init__(self, parent, flags=None):
        """ Creates a new dashboard view"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Dashboard, self).__init__(parent, flags)
        self.settings = self.get_dashboard_settings()
        self.setupUi()

    def dosearch(self):
        """Call to search view"""
        self.parent().display_view(
            'search',
            {'term': self.lSearch.text().toUtf8(),
            'collection': self.settings['quicksearch']})

    def get_dashboard_settings(self):
        """Calculates the dashboard settings"""
        # TODO Settings and default values calculation must go inside
        # collection
        settings = {}
        collections = self.parent().collection.collections
        stored = self.parent().collection.get_property('dashboard')
        items = []
        for collection in collections.values():
            image = collection.get_image()
            if image is None:
                image = ":folder.png"
            items.append(
                {'class': 'link', 'name': collection.get_name(),
                 'path': 'view/collection/collection/' + collection.get_id(),
                 'image': image}
            )
        # TODO allow personalization of the new entry button?
        if len(collections) > 0:
            if stored is not None:
                main_collection = collections[stored['lastcollection']]
                settings['quicksearch'] = stored['quicksearch']

            else:
                main_collection = collections.values()[0]
                settings['quicksearch'] = main_collection.get_id()
            settings['lastcollection'] = main_collection.get_id()
            items.extend([
                {'class': 'spacer'},
                {'class': 'line'},
                {'class': 'link',
                 'name': str(self.tr('New <b>%s</b>')) %
                    main_collection.get_name(),
                 'path': 'view/add/collection/' + main_collection.get_id(),
                 'image': ':/add.png'}
            ])
        else:
            settings['lastcollection'] = None

        settings['items'] = items
        # Override with stored settings:

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
            self.dosearch)

        Topbar(widget=self.topbar, icon=':ico/dashboard.png',
               title=self.tr("Dashboard").toUpper())
        self._loadToolbar()
        self.listWidget.connect(
            self.listWidget,
            QtCore.SIGNAL(_fromUtf8("itemClicked(QListWidgetItem *)")),
            self.goto_selected)

    def _loadToolbar(self):
        """ Creates the toolbar for the view, this function must be
         called after the Ui_Form.setupUi has been called."""
        items = self.settings['items']
        CustomToolbar(self.toolbar, items, self._toolbarCallback)

    def _toolbarCallback(self, uri):
        """Callback for the toolbar"""
        self.parent().collector_uri_call(uri)

    def last_files(self, listContainer):
        """Renders the last files"""
        collection_id = self.settings['lastcollection']
        if collection_id is not None:
            collection = self.parent().collection.get_collection(collection_id)
            label = collection.get_name()
            self.lLastItems.setText(str(self.tr("Last %s")) % label)
            lastObjects = collection.get_last(40)
            for i in lastObjects:
                text = i[collection.schema.default]
                item = FitxaListItem(i['id'], text != '' and
                                     text or str(self.tr('Entry %d')) %
                                     i['id'])
                listContainer.addItem(item)
        else:
            self.lLastItems.setText(
                self.tr("Warning: No collection available!"))

    @QtCore.pyqtSlot()
    def reload(self):
        """Reloads the dashboard view"""
        #TODO test and try!
        self.settings = self.get_dashboard_settings()
        self.listWidget.clear()
        self.last_files(self.listWidget)
        #TODO reload the new entry button

    def goto_selected(self, s):
        """Goes to the selected item"""
        self.parent().display_view(
            'fitxa',
            {'item': s.id, 'collection': self.settings['lastcollection']})


class DashboardView(Page):
    """Dashboard view"""

    def get_widget(self, params):
        dashboardWidget = Ui_Dashboard(self.parent)
        return dashboardWidget
