# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.fitxa import Ui_File
from ui.helpers.customtoolbar import CustomToolbar, Topbar
from ui.widgetprovider import WidgetProvider
from ui.helpers.filedata import FileDataWidget


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_Fitxa(QtGui.QWidget, Ui_File):

    def __init__(self, item, collection, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Fitxa, self).__init__(parent, flags)
        # TODO obtain full item, not only the title
        self.item = item
        self.collection = self.parent().collection.getCollection(collection)
        self.setupUi()

    def setupUi(self):
        super(Ui_Fitxa, self).setupUi(self)
        item = self.item
        obj = self.collection.get(item)
        self.collection.loadReferences(obj)
        self.fontLabel = QtGui.QFont()
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)
        schema = self.collection.schema
        Topbar(widget=self.topbar, icon=self.collection.schema.ico,
               title=self.collection.schema.name.upper() + ' > ' +
                obj[schema.default])
        self.progressBar.hide()
        self.data_widget = FileDataWidget(schema, obj)
        self.scrollArea.setWidget(self.data_widget)

        self._loadToolbar()

    def _loadToolbar(self):
        quick = [
            {'class':'link', 'name': self.tr('Dashboard'),
             'path': 'view/dashboard', 'image': ':/dashboard.png'},
            {'class':'link', 'name': self.collection.schema.name,
             'path': 'view/collection/collection/' + self.collection.name,
             'image': ':/boards.png'},
            {'class': 'spacer'},
            {'class': 'line'},
            {'class':'link', 'name':self.tr('Options'),
             'path': 'action/options',
             'image': ':/add.png'},
            # {'class':'link', 'name': 'Delete', 'path': 'action/delete',
             # 'image': ':/delete.png'},
            # {'class':'link', 'name': 'Edit', 'path': 'view/edit/collection/' +
            #  self.collection.name + '/item/' + str(self.item),
            #  'image': ':/edit.png'},
        ]
        CustomToolbar(self.toolbar, quick, self._linkactivated)
        menu = QtGui.QMenu(self.topbar)
        menu.addAction(QtGui.QAction(
            QtGui.QIcon(':/edit.png'),
            self.tr("Edit"), self,
            statusTip=self.tr("Edit file"),
            triggered=lambda: self.parent().display_view(
                'edit',
                params={"collection": self.collection.name,
                        "item": str(self.item)}))
        )
        menu.addAction(QtGui.QAction(
            QtGui.QIcon(':/delete.png'),
            self.tr("Delete"), self,
            statusTip=self.tr("Delete file"),
            triggered=lambda: self.delete())
        )
        self.actions_menu = menu

    def _linkactivated(self, uri):
        params = self.parent().collector_uri_call(uri)
        if params is not None:
            action = params['action']
            if action == 'options':
                self.actions_menu.popup(QtGui.QCursor.pos())
            # if action == 'delete':
            #     self.delete()

    def delete(self):
        self.collection.delete(self.item)
        self.parent().display_view('dashboard')


class FitxaView(WidgetProvider):

    def getWidget(self, params):
        collection = params['collection']
        item = params['item']
        return Ui_Fitxa(item, collection, self.parent)
