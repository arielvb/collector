# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.fitxa import Ui_Form
from ui.helpers.customtoolbar import CustomToolbar, Topbar
from ui.widgetprovider import WidgetProvider
from engine.fields import FieldImage


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
            item.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse |
                                         QtCore.Qt.TextSelectableByMouse)
        item.setText(text)
        item.setObjectName(_fromUtf8(text))
        return item

    def createField(self, label, text):
        columnspan = 1
        column = 0
        rowspan = 1
        #TODO add support for multiavalue fields
        itemLabel = self.createLabel(label, True)
        self.fieldsLayout.addWidget(itemLabel, self.row, column,
                                    rowspan, columnspan)
        column += 1
        if not isinstance(text, list):
            text = [text]
        for i in text:
            item = self.createLabel(i)
            self.fieldsLayout.addWidget(item, self.row, column,
                                        rowspan, columnspan)
            self.row += 1
        self.row += 1

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
               title=self.collection.schema.name.upper() + ' > ' + obj['name'])
        # self.lWindowTitle.setText(schema.name.upper() + ' > ')
        # self.lTitle.setText(obj['name'])
        for field in schema.order:
            if field != 'image':
                value = field in obj and obj[field] or ''
                self.createField(schema.fields[field]['name'], value)
        # self.createField('Name', obj['name'])
        # self.createField('Designer/s', obj['designer'])
        # self.createField('Artist/s', obj['artist'])

        # TODO set image: we need to store it somewhere...
        #  but where is the best place?
        if 'image' in obj:
            image = FieldImage('image', value=value)
            image.setValue(obj['image'])
            path = image.getValue()
            pixmap = None
            if path != '':
                pixmap = QtGui.QPixmap(path)
            # Check if the file doensn't have image or the image file
            #  doesn't exists
            if pixmap is None or pixmap.isNull():
                pixmap = QtGui.QPixmap(_fromUtf8(':box.png'))
            scaled = pixmap.scaled(150, 150, QtCore.Qt.KeepAspectRatio)
            self.image.setPixmap(scaled)
        else:
            self.image.hide()
        self._loadToolbar()

    def _loadToolbar(self):
        quick = [
            {'class':'link', 'name': 'Dashboard',
             'path': 'view/dashboard', 'image': ':/dashboard.png'},
            {'class':'link', 'name': self.collection.schema.name,
             'path': 'view/collection/collection/' + self.collection.name,
             'image': ':/boards.png'},
            {'class': 'spacer'},
            {'class': 'line'},
            {'class':'link', 'name': 'Delete', 'path': 'action/delete',
             'image': ':/delete.png'},
            {'class':'link', 'name': 'Edit', 'path': 'view/edit/collection/' +
             self.collection.name + '/item/' + str(self.item),
             'image': ':/edit.png'},
        ]
        CustomToolbar(self.toolbar, quick, self._linkactivated)

    def _linkactivated(self, uri):
        params = self.parent().collector_uri_call(uri)
        if params is not None:
            action = params['action']
            if action == 'delete':
                self.delete()

    def delete(self):
        self.collection.delete(self.item)
        self.parent().display_view('dashboard')


class FitxaView(WidgetProvider):

    def getWidget(self, params):
        collection = params['collection']
        item = params['item']
        return Ui_Fitxa(item, collection, self.parent)
