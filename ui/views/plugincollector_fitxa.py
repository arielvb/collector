# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QMessageBox, QMenu, QAction, QIcon, QCursor
from ui.gen.fitxa import Ui_File
from ui.helpers.customtoolbar import CustomToolbar, Topbar
from ui.widgetprovider import WidgetProvider
from ui.helpers.filedata import FileDataWidget
from ui.workers.search import Worker_FileLoader, STATUS_OK
import webbrowser


class Ui_PluginFile(QWidget, Ui_File):

    worker = Worker_FileLoader()

    def __init__(self, file_id, plugin, referer, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_PluginFile, self).__init__(parent, flags)
        self.id = file_id
        self.plugin = self.parent().plugin_manager.get(plugin)
        self.referer = referer
        self.setupUi()

    def setupUi(self):
        super(Ui_PluginFile, self).setupUi(self)

        self.scrollArea.show()

        schema = self.plugin.schema
        # TODO use plugin ico or see:
        # http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/qwebsettings.html#iconForUrl
        self.topbarHelper = Topbar(widget=self.topbar, icon=":/ico/folder.png",
               title=schema.name.upper() + ' > ' + self.tr("Loading..."))

        self.worker.load_complete.connect(self.load_complete)
        self._loadToolbar()
        self.search()

    @QtCore.pyqtSlot()
    def search(self):
        """Loads the content"""
        self.progressBar.show()
        self.worker.search(self.id, self.plugin.get_id())

    def _loadToolbar(self):
        quick = [
            {'class':'link', 'name': self.tr('Go back'),
             'path': 'action/back', 'image': ':/back.png'},
            {'class':'link', 'name': self.tr('Dashboard'),
             'path': 'view/dashboard', 'image': ':/dashboard.png'},
            {'class': 'spacer'},
            # {'class':'link', 'name': self.tr('View in browser'),
            #  'path': 'action/browser', 'image': ':/add.png'},
            # {'class':'link', 'name': self.tr('Reload'),
            #  'path': 'action/reload', 'image': ':/add.png'},
            {'class':'link', 'name': self.tr('Options'),
             'path': 'action/options', 'image': ':/add.png'},
        ]
        CustomToolbar(self.toolbar, quick, self._linkactivated)
        menu = QMenu(self.topbar)
        #TODO implement add to my collection action
        menu.addAction(QAction(
            QIcon(':/add.png'),
            self.tr("Add"), self,
            statusTip=self.tr("Add to my collection"),
            triggered=lambda: "a")
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
        self.actions_menu = menu


    def _linkactivated(self, uri):
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
            # elif action == 'reload':
            #     self.search()
            # elif action == 'browser':
            #     webbrowser.open(self.id)

    def load_complete(self, results):
        """Updates the view with the results of the worker"""
        self.progressBar.hide()
        if results.status != STATUS_OK:
            QMessageBox.warning(self,
                self.tr("Collector"),
                self.tr("Ooops!\nSomething happened and the search" +
                        " could'nt be completed."))
        else:
            self.results = results.results
            schema = self.plugin.schema
            self.data_widget = FileDataWidget(schema,
             results.results)
            self.scrollArea.setWidget(self.data_widget)
            self.scrollArea.show()
            self.topbarHelper.set_title(schema.name.upper() +
             ' > ' + results.results[schema.default])


class PluginFileView(WidgetProvider):

    def getWidget(self, params):
        plugin = params['plugin']
        item = params['id']
        referer = params['referer']
        return Ui_PluginFile(item, plugin, referer, self.parent)
