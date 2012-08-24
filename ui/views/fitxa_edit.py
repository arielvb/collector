# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.fitxa_edit import Ui_Form
from ui.helpers.customtoolbar import CustomToolbar
from PyQt4.Qt import qDebug

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_Fitxa_Edit(QtGui.QWidget, Ui_Form):

    row = 0

    def __init__(self, item, collection, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Fitxa_Edit, self).__init__(parent, flags)
        self.item = item
        self.collection = self.parent().collection.getCollection(collection)
        self.setupUi(item)

    def setupUi(self, item):
        super(Ui_Fitxa_Edit, self).setupUi(self)
        self._loadToolbar()
        # Obtain the object
        self.obj = self.collection.get(item)
        obj = self.obj
        self.fontLabel = QtGui.QFont()
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)
        schema = self.collection.schema
        self.lWindowTitle.setText(schema.name.upper() + ' > ')
        self.lTitle.setText(obj['name'])
        self.fitxa_fields = {}
        for field in schema.order:
            value = field in obj and obj[field] or ''
            widgets = self.createField(schema.fields[field]['name'], value)
            self.fitxa_fields[field] = widgets
        #self.bCancel.connect(self.bCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda: self.parent().displayView('fitxa', {'item': obj['name']}))
        #self.bSave.connect(self.bSave, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda: self.save())

    def createLabel(self, text, label=False):
        item = QtGui.QLabel(self)
        if label:
            item.setFont(self.fontLabel)
        else:
            item.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        item.setText(text)
        item.setObjectName(_fromUtf8(text))
        return item

    def createLineEdit(self, text, label=False):
        item = QtGui.QLineEdit(self)
        #if label:
        #    item.setFont(self.fontLabel)
        #else:
        #    item.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextSelectableByMouse)
        item.setText(text)
        item.setObjectName(_fromUtf8(text))
        return item

    def createField(self, label, text):
        columnspan = 1
        column = 0
        rowspan = 1
        itemLabel = self.createLabel(label, True)
        # TODO image schema must allow choose file from the os
        # usign QtGui.QFileDialog()
        self.fieldsLayout.addWidget(itemLabel, self.row, column, rowspan, columnspan)
        column += 1
        if not isinstance(text, list):
            text = [text]
        # If is allowed multiple values for each field, an iteration is needed
        widgets = []
        for i in text:
            item = self.createLineEdit(i)
            widgets.append(item)
            self.fieldsLayout.addWidget(item, self.row, column, rowspan, columnspan)
            self.row += 1
        self.row += 1
        return widgets

    def _loadToolbar(self):
        quick = [
            {'class':'link', 'name': 'Cancel', 'path': 'cancel', 'image': ':/back.png'},
            {'class': 'spacer'},
            {'class':'link', 'name': 'Save', 'path': 'save', 'image': ':/save.png'},
        ]
        CustomToolbar(self.toolbar, quick, self._linkactivated)

    def _linkactivated(self, uri):
        qDebug('Uri called: ' + uri)
        if uri == 'collector:save':
            self.save()
        elif uri == 'collector:cancel':
            self.parent().displayView('fitxa', {'item': self.item, 'collection': self.collection.name})

    def save(self):
        qDebug('Saving!')
        schema = self.collection.schema
        data = {}
        for field in schema.order:
            fields = self.fitxa_fields[field]
            # TODO compression list
            values = []
            for i in fields:
                values.append(str(i.text()))
            if not schema.isMultiple(field):
                values = values[0]
            data[field] = values
        data['id'] = self.obj['id']
        self.collection.save(data)
        self.parent().displayView('fitxa', {'item': data['id'], 'collection': self.collection.name})
        qDebug(str(data))

        #pass


class FitxaEditView():

    def __init__(self, parent):
        self.parent = parent

    def run(self, params):
        item = params['item']
        collection = params['collection']
        fitxaWidget = Ui_Fitxa_Edit(item, collection, self.parent)
        self.parent.setCentralWidget(fitxaWidget)
