# -*- coding: utf-8 -*-
#pylint: disable-msg=E1101,E0611
# E0611: No name 'QtCore' in module 'PyQt4'
# E1101: Module 'PyQt4.QtCore' has no ...
"""The plugin file view and widget"""

from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QMessageBox, QMenu, QAction, QIcon, QCursor
from collector.ui.gen.fitxa import Ui_File
from collector.ui.helpers.customtoolbar import CustomToolbar, Topbar
from collector.ui.widgetprovider import WidgetProvider
from collector.ui.helpers.filedata import FileDataWidget
from collector.ui.workers.search import Worker_FileLoader, STATUS_OK
from collector.core.controller import Collector
import webbrowser


class Ui_PluginFile(QWidget, Ui_File):
    """The Plugin File Widget"""

    worker = Worker_FileLoader()

    def __init__(self, file_id, plugin, referer, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_PluginFile, self).__init__(parent, flags)
        self.id = file_id
        # TODO this must be a parameter
        self.collection = 'boardgames'
        self.plugin = self.parent().plugin_manager.get(plugin)
        self.data_widget = None
        self.data = None
        self.referer = referer
        self.setupUi()
        self.actions_menu = self._menu()

    def setupUi(self):
        """The ui build process"""
        super(Ui_PluginFile, self).setupUi(self)

        self.scrollArea.show()

        schema = self.plugin.schema
        self.topbarHelper = Topbar(
            widget=self.topbar,
            icon= self.plugin.icon,
            title=schema.name.upper() + ' > ' + self.tr("Loading..."))

        self.worker.load_complete.connect(self.load_complete)
        self._loadToolbar()
        self.search()

    @QtCore.pyqtSlot()
    def add_to_my_collection(self):
        """Add the current plugin file to the user collection"""
        if self.data is not None:
            collector = Collector.get_instance()
            result = collector.add(self.data, self.collection,
                          use_mapping=self.plugin.get_id())
            if result is not None:
                #Ok
                # TODO notify and ask to go?
                pass
            else:
                QMessageBox.warning(self,
                self.tr("Collector"),
                self.tr("Ooops, an error ocurred" +
                        " and no data couldn't be added."))
        else:
            QMessageBox.warning(self,
                self.tr("Collector"),
                self.tr("The content isn't yet available," +
                        " and no data couldn't be added."))

    @QtCore.pyqtSlot()
    def search(self):
        """Loads the content"""
        self.progressBar.show()
        self.data = None
        self.worker.search(self.id, self.plugin.get_id())

    def _menu(self):
        """Creates the menu for the options action"""
        menu = QMenu(self.topbar)
        #TODO implement add to my collection action
        menu.addAction(QAction(
            QIcon(':/add.png'),
            self.tr("Add"), self,
            statusTip=self.tr("Add to my collection"),
            triggered=self.add_to_my_collection)
        )
        menu.addAction(QAction(
            QIcon(':/reload.png'),
            self.tr("Reload"), self,
            statusTip=self.tr("Reload the file."),
            triggered=self.search)
        )

        menu.addAction(QAction(
            QIcon(':/browser.png'),
            self.tr("View in browser"), self,
            statusTip=self.tr("View in your browser"),
            triggered=lambda: webbrowser.open(self.id))
        )
        return menu

    def _loadToolbar(self):
        quick = [
            {'class':'link', 'name': self.tr('Go back'),
             'path': 'action/back', 'image': ':/back.png'},
            {'class':'link', 'name': self.tr('Dashboard'),
             'path': 'view/dashboard', 'image': ':/dashboard.png'},
            {'class': 'spacer'},
            {'class':'link', 'name': self.tr('Options'),
             'path': 'action/options', 'image': ':/add.png'},
        ]
        CustomToolbar(self.toolbar, quick, self._linkactivated)

    def _linkactivated(self, uri):
        """Callback for the toolbar"""
        params = self.parent().collector_uri_call(uri)
        #TODO check action is go back
        if params is not None:
            action = params['action']
            if action == 'options':
                self.actions_menu.popup(QCursor.pos())
            # action = params['action']
            if action == 'back':
                self.parent().display_view(self.referer['view'],
                                           self.referer['params'])

    def load_complete(self, results):
        """Updates the view with the results of the worker"""
        self.progressBar.hide()
        if results.status != STATUS_OK:
            QMessageBox.warning(self,
                self.tr("Collector"),
                self.tr("Ooops!\nSomething happened and the search" +
                        " could'nt be completed."))
        else:
            self.data = results.results
            schema = self.plugin.schema
            self.data_widget = FileDataWidget(schema,
             self.data, self.parent())
            self.scrollArea.setWidget(self.data_widget)
            self.scrollArea.show()
            self.topbarHelper.set_title(schema.name.upper() +
             ' > ' + self.data[schema.default])


class PluginFileView(WidgetProvider):

    def get_widget(self, params):
        plugin = params['plugin']
        item = params['id']
        referer = params['referer']
        return Ui_PluginFile(item, plugin, referer, self.parent)
