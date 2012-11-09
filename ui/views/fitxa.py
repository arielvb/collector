# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.fitxa import Ui_File
from ui.helpers.customtoolbar import CustomToolbar, Topbar
from ui.widgetprovider import WidgetProvider
from ui.helpers.filedata import FileDataWidget
from ui.workers.search import Worker_Discover, Worker_Queue
from engine.collector import Collector


class Ui_Fitxa(QtGui.QWidget, Ui_File):

    def __init__(self, item, collection, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Fitxa, self).__init__(parent, flags)
        self.item = item
        self.collection = self.parent().collection.get_collection(collection)
        self.setupUi()
        self.worker = Worker_Discover()
        self.workerQ = None

    def setupUi(self):
        super(Ui_Fitxa, self).setupUi(self)
        item = self.item
        obj = self.collection.get(item)
        obj = self.collection.load_references(obj)
        self.obj = obj
        self.fontLabel = QtGui.QFont()
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)
        schema = self.collection.schema
        Topbar(widget=self.topbar, icon=self.collection.schema.ico,
               title=self.collection.schema.name.upper() + ' > ' +
                obj[schema.default])
        self.progressBar.hide()
        self.data_widget = FileDataWidget(schema, obj, self.parent())
        self.scrollArea.setWidget(self.data_widget)
        self._loadToolbar()

    def _loadToolbar(self):
        image = self.collection.get_image() or ':folder.png'
        quick = [
            {'class':'link', 'name': self.tr('Dashboard'),
             'path': 'view/dashboard', 'image': ':/dashboard.png'},
            {'class':'link', 'name': self.collection.schema.name,
             'path': 'view/collection/collection/' + self.collection.get_id(),
             'image': image},
            {'class': 'spacer'},
            {'class': 'line'},
            {'class':'link', 'name':self.tr('Options'),
             'path': 'action/options',
             'image': ':/add.png'},
        ]
        CustomToolbar(self.toolbar, quick, self._linkactivated)
        menu = QtGui.QMenu(self.topbar)
        menu.addAction(QtGui.QAction(
            QtGui.QIcon(':/edit.png'),
            self.tr("Edit"), self,
            statusTip=self.tr("Edit file"),
            triggered=lambda: self.parent().display_view(
                'edit',
                params={"collection": self.collection.get_id(),
                        "item": str(self.item)}))
        )
        menu.addAction(QtGui.QAction(
            self.tr("Autocomplete"),
            self,
            statusTip=self.tr("Autocomplete"),
            triggered=self.autocomplete
            )
        )
        menu.addAction(QtGui.QAction(
            QtGui.QIcon(':/delete.png'),
            self.tr("Delete"), self,
            statusTip=self.tr("Delete file"),
            triggered=self.delete)
        )
        menu.addAction(QtGui.QAction(
            QtGui.QIcon(':/add.png'),
            self.tr("New entry"), self,
            statusTip=self.tr("New entry"),
            triggered=lambda: self.parent().display_view(
                'add',
                {'collection': self.collection.get_id()})
            )
        )
        self.actions_menu = menu

    def _linkactivated(self, uri):
        """Callback called when a link of the toolbar is activated"""
        params = self.parent().collector_uri_call(uri)
        if params is not None:
            action = params['action']
            if action == 'options':
                self.actions_menu.popup(QtGui.QCursor.pos())
            # if action == 'delete':
            #     self.delete()

    def autocomplete(self):
        """Launches to the autocomplete proces"""
        self.progress = QtGui.QProgressDialog(
                self.tr("Looking for data (Step 1/3)"),
                self.tr("Abort"),
                0,
                0)
        self.progress.canceled.connect(self.abortautocomplete)
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.show()
        self.worker.searchComplete.connect(self.showalternatives)
        self.worker.search(self.obj[self.collection.schema.default])

    def showalternatives(self, results):
        """Choose the alternatives to autocomplete"""
        # self.progress.hide()
        self.progress.setLabelText("Loading data (Step 2/3)")
        # self.progress = None
        if len(results.results) > 0:
            # TODO display alternatives window
            alternatives = results.results

            self.workerQ = Worker_Queue(alternatives)
            self.workerQ.complete.connect(self.docomplete)
            self.workerQ.start()
            # Collector.getInstance().complete(
            #     self.collection.get_id(),
            #     self.obj['id'],
            #     alternatives)
            # self.parent().display_view(
            #     'comparefile',
            #     params={'source': self.obj,
            #             'new': alternatives[0]}
            # )
        else:
            QtGui.QMessageBox.warning(self, self.tr("Collector"),
                self.tr("No data found"))

    def docomplete(self, data):
        """aaaaa"""
        self.progress.setLabelText("Autocomplete running (Step 3/3)")
        # self.progress.setCancelButton(0)
        if isinstance(data, list):
            # TODO allow multiple values
            data = data[0]
        if not isinstance(data, dict):
            self.progress.hide()
            # TODO raise error
        Collector.get_instance().complete(
            self.collection.get_id(),
            self.obj['id'],
            data)
        self.progress.hide()
        self.parent().display_view('fitxa', params={
            'item': self.obj['id'],
            'collection': self.collection.get_id()
            }
        )

    def abortautocomplete(self):
        if self.worker is not None:
            self.worker.terminate()
            self.worker.wait()

    def delete(self):
        """Deletes the current item from the collection"""
        # TODO! ask confirmation to the user.
        result = QtGui.QMessageBox.question(
            self,
            self.tr("Delete item"),
            self.tr("Are you sure you want to remove this file?"),
            QtGui.QMessageBox.Yes,
            QtGui.QMessageBox.No)
        if result == QtGui.QMessageBox.Yes:
            self.collection.delete(self.item)
            self.parent().display_view('dashboard')


class FitxaView(WidgetProvider):

    def get_widget(self, params):
        collection = params['collection']
        item = params['item']
        return Ui_Fitxa(item, collection, self.parent)
