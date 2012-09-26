# -*- coding: utf-8 -*-

from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QMessageBox
from ui.gen.fitxa import Ui_File
from ui.helpers.customtoolbar import CustomToolbar, Topbar
from ui.widgetprovider import WidgetProvider
from ui.helpers.filedata import FileDataWidget
from ui.workers.search import Worker_FileLoader, STATUS_OK

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_PluginFile(QWidget, Ui_File):


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
        # TODO use plugin ico
        self.topbarHelper = Topbar(widget=self.topbar, icon=":/ico/folder.png",
               title=schema.name.upper() + ' > ' + self.tr("Loading..."))

        self.parent().worker.complete.connect(lambda r: self.load_complete(r))

        self._loadToolbar()

    def search(self):
        self.worker.search(self.id, self.plugin.get_id())

    def _loadToolbar(self):
        quick = [
            {'class':'link', 'name': self.tr('Go back'),
             'path': 'action/back', 'image': ':/back.png'},
            {'class':'link', 'name': self.tr('Dashboard'),
             'path': 'view/dashboard', 'image': ':/dashboard.png'},
            {'class': 'spacer'},
        ]
        CustomToolbar(self.toolbar, quick, self._linkactivated)

    def _linkactivated(self, uri):
        params = self.parent().collector_uri_call(uri)
        #TODO check action is go back
        self.parent().display_view(self.referer['view'], self.referer['params'])

    def load_complete(self, results):
        """Updates the view with the results of the worker"""
        self.progressBar.hide()
        if results.status != STATUS_OK:
            QMessageBox.warning(self,
                self.tr("Collector"),
                self.tr("Ooops!\nSomething happened and the search" +
                        " could'nt be completed."))
        else:
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
