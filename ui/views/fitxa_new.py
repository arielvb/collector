# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.fitxa_edit import Ui_Form
from ui.helpers.customtoolbar import CustomToolbar
from ui.widgetprovider import WidgetProvider
from PyQt4.Qt import qDebug

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_Fitxa_New(QtGui.QWidget, Ui_Form):

    row = 0

    def __init__(self, collection, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Fitxa_New, self).__init__(parent, flags)
        self.item = None
        self.collection = self.parent().collection.getCollection(collection)
        self.setupUi()

    def setupUi(self):
        super(Ui_Fitxa_New, self).setupUi(self)
        self._loadToolbar()
        # Obtain the object
        self.fontLabel = QtGui.QFont()
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)
        schema = self.collection.schema
        self.lWindowTitle.setText(schema.name.upper() + ' > ')
        self.lTitle.setText('New entry')
        self.fitxa_fields = {}
        for field in schema.order:
            widgets = self.createField(schema.fields[field]['name'], '')
            self.fitxa_fields[field] = widgets

    def createLabel(self, text, label=False):
        item = QtGui.QLabel(self)
        if label:
            item.setFont(self.fontLabel)
        else:
            item.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse
                | QtCore.Qt.TextSelectableByMouse)
        item.setText(text)
        item.setObjectName(_fromUtf8(text))
        return item

    def createLineEdit(self, text, label=False):
        item = QtGui.QLineEdit(self)
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
        self.fieldsLayout.addWidget(itemLabel,
            self.row, column, rowspan, columnspan)
        column += 1
        if not isinstance(text, list):
            text = [text]
        # If is allowed multiple values for each field, an iteration is needed
        widgets = []
        for i in text:
            item = self.createLineEdit(i)
            widgets.append(item)
            self.fieldsLayout.addWidget(item,
                self.row, column, rowspan, columnspan)
            self.row += 1
        self.row += 1
        return widgets

    def _loadToolbar(self):
        quick = [
            {'class':'link', 'name': 'Cancel',
                'path': 'action/cancel', 'image': ':/back.png'},
            {'class': 'spacer'},
            {'class':'link', 'name': 'Save',
                'path': 'action/save', 'image': ':/save.png'},
        ]
        CustomToolbar(self.toolbar, quick, self._linkactivated)

    def _linkactivated(self, uri):
        qDebug('Uri called: ' + uri)
        params = self.parent().collectorURICaller(uri)
        action = params['action']
        if action == 'save':
            self.save()
        elif action == 'cancel':
            # TODO return to referer parameter?
            self.parent().displayView('collection',
                {'collection': self.collection.name})

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
            if not schema.isMultivalue(field):
                values = values[0]
            data[field] = values
        # data['id'] = self.obj['id']
        self.collection.save(data)
        self.parent().displayView('fitxa',
            {'item': data['id'], 'collection': self.collection.name})
        qDebug(str(data))


class FitxaNewView(WidgetProvider):

    def getWidget(self, params):
        collection = params['collection']
        return Ui_Fitxa_New(collection, self.parent)
