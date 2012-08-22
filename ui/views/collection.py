# -*- coding: utf-8 -*-
from ui.gen.collection_items import Ui_Form
from PyQt4 import QtCore, QtGui
from ui.helpers.customtoolbar import CustomToolbar, Topbar


class FitxaTableItem(QtGui.QTableWidgetItem):

    def __init__(self, itemId):
        self.id = itemId
        super(FitxaTableItem, self).__init__()

    def getObjectId(self):
        return self.id


class Ui_Collection(QtGui.QWidget, Ui_Form):

    _table_headers = 0
    _table_items = 0

    def __init__(self, parent, collection, flags=None):
        """ Creates a new dashboard view"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Collection, self).__init__(parent, flags)
        self.setupUi(self)
        self.collection = self.parent().collection.getInstance().getCollection(collection)
        self.schema = self.collection.schema
        self.objects = self.collection.getAll()
        self.customize()

    def customize(self):
        #Topbar
        # TODO title collection name must be a parameter
        Topbar(widget=self.topbar, icon='boards.png',
            title=self.collection.schema.name.upper())

        # Toolbar
        items = [
                {'class':'link', 'name': 'Dashboard', 'path': 'dashboard', 'image': ':/dashboard.png'},
                {'class': 'spacer'},
                {'class': 'line'},
                # TODO i10n
                {'class':'link', 'name': 'New <b>' + self.collection.schema.name + '</b> entry', 'path': 'collection/' + self.collection.name + '/add', 'image': ':/add.png'},
        ]
        CustomToolbar(self.toolbar, items, self._toolbarCallback)
        # +1 (id field)
        self.tableWidget.setColumnCount(len(self.schema.order))
        self.tableWidget.setRowCount(len(self.objects))
        header = self.schema.order
        for item in header:
                self.createHeaderItem(self.schema.fields[item]['name'])
        for item in self.objects:
            self.createTableRow(item, header)

        # Connections
        QtCore.QObject.connect(self.tableWidget, QtCore.SIGNAL("itemDoubleClicked(QTableWidgetItem*)"), self._itemSelected)

    def _toolbarCallback(self, uri):
        if uri == 'collector:dashboard':
            self.parent().displayView('dashboard')

    def createHeaderItem(self, text):
        item = QtGui.QTableWidgetItem()
        item.setText(text)
        self.tableWidget.setHorizontalHeaderItem(self._table_headers, item)
        self._table_headers += 1

    def createTableRow(self, items, orderedKeys):
        """ items is a list, and each item of the list can be a string or a list """
        row = self._table_items
        column = 0
        for key in orderedKeys:
            item = FitxaTableItem(items['id'])
            #TODO allow list elements
            value = ''
            if key in items:
                value = items[key]
            if not isinstance(value, list):
                item.setText(str(value))
            else:
                more = len(value) - 1
                more_text = ''
                if  more > 0:
                    more_text = " and " + str(more) + " more"
                item.setText(str(value[0]) + more_text)
            self.tableWidget.setItem(row, column, item)
            column += 1
        self._table_items += 1

    def _itemSelected(self, tableItem):
        itemId = tableItem.getObjectId()
        from PyQt4.Qt import qDebug; qDebug(str(itemId))
        self.parent().displayView('fitxa', {'item': tableItem.getObjectId(), 'collection': self.collection.name})


class CollectionView():

    def __init__(self, parent):
        self.parent = parent

    def run(self, params={}):
        from PyQt4.Qt import qDebug; qDebug(str(params))
        self.parent.fitxa = None
        widget = Ui_Collection(self.parent, collection=params['collector:collection'])
        #ui = Ui_Form()
        #ui.setupUi(widget)
        self.parent.setCentralWidget(widget)