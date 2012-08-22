# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.fitxa import Ui_Form
from ui.helpers.customtoolbar import CustomToolbar, Topbar
from PyQt4.Qt import qDebug  # Debug!!!

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_Fitxa(QtGui.QWidget, Ui_Form):

    row = 0

    def __init__(self, item, collection, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Fitxa, self).__init__(parent, flags)
        # TODO obtain full item, not only the title
        self.item = item
        self.collection = self.parent().collection.getCollection(collection)
        self.setupUi()

    def createLabel(self, text, label=False):
        item = QtGui.QLabel(self)
        if label:
            item.setFont(self.fontLabel)
        else:
            item.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        item.setText(text)
        item.setObjectName(_fromUtf8(text))
        return item

    def createField(self, label, text):
        columnspan = 1
        column = 0
        rowspan = 1
        #TODO add support for multiavalue fields
        itemLabel = self.createLabel(label, True)
        self.fieldsLayout.addWidget(itemLabel, self.row, column, rowspan, columnspan)
        column += 1
        if not isinstance(text, list):
            text = [text]
        for i in text:
            item = self.createLabel(i)
            self.fieldsLayout.addWidget(item, self.row, column, rowspan, columnspan)
            self.row += 1
        self.row += 1

    def setupUi(self):
        super(Ui_Fitxa, self).setupUi(self)
        item = self.item
        obj = self.collection.get(item)
        from PyQt4.Qt import qDebug; qDebug(str(obj))
        self.fontLabel = QtGui.QFont()
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)
        schema = self.collection.schema
        Topbar(widget=self.topbar, icon='boards.png',
            title=self.collection.schema.name.upper() + ' > ' + obj['name'])
        # self.lWindowTitle.setText(schema.name.upper() + ' > ')
        # self.lTitle.setText(obj['name'])
        for field in schema.order:
            if field != 'image':
                value = field in obj and obj[field] or ''
                self.createField(schema.fields[field]['name'], value)
        #self.createField('Name', obj['name'])
        #self.createField('Designer/s', obj['designer'])
        #self.createField('Artist/s', obj['artist'])

        # TODO set image: we need to store it somewhere...
        # but where is the best place?
        import os
        if 'image' in obj:
            self.image.setPixmap(
                    QtGui.QPixmap(os.path.join(os.path.dirname(__file__),
                        obj['image'])
                        )
                    )
        else:
            self.image.hide()
        self._loadToolbar()
        # Connect dashboard and edit button
        #self.bDashboard.connect(self.bDashboard, QtCore.SIGNAL(_fromUtf8("linkActivated(QString)")), lambda s: self.parent().viewDashboard())
        #self.bEdit.connect(self.bEdit, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda: self.parent().displayView('fitxa_edit', {'item': item}))

    def _loadToolbar(self):
        quick = [
            {'class':'link', 'name': 'Dashboard', 'path': 'dashboard', 'image': ':/dashboard.png'},
            {'class':'link', 'name': 'Boardgames', 'path': 'collection/' + self.collection.name, 'image': ':/boards.png'},
            {'class': 'spacer'},
            {'class': 'line'},
            {'class':'link', 'name': 'Edit', 'path': 'collection/' + self.collection.name + '/edit', 'image': ':/edit.png'},
        ]
        CustomToolbar(self.toolbar, quick, self._linkactivated)

    def _linkactivated(self, uri):
        qDebug('Uri called: ' + uri)
        collection = self.collection.name
        if uri == 'collector:dashboard':
            self.parent().displayView('dashboard')
        elif uri == 'collector:collection/' + collection + '/edit':
            self.parent().displayView('fitxa_edit', {'item': self.item, 'collection': self.collection.name})
        elif uri == 'collector:collection/' + collection:
            #TODO this code is from dashboard:_toolbarCallback, refractor to a single place
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
            self.parent().displayView('collection', params)


class FitxaView():

    def __init__(self, parent):
        self.parent = parent

    def run(self, params):
        collection = params['collection']
        item = params['item']
        fitxaWidget = Ui_Fitxa(item, collection, self.parent)
        self.parent.setCentralWidget(fitxaWidget)
