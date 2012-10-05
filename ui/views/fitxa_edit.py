# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.fitxa_edit import Ui_Form
from ui.helpers.customtoolbar import CustomToolbar, Topbar
from ui.widgetprovider import WidgetProvider
from ui.helpers.fields import FieldWidgetManager


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
        self.man = FieldWidgetManager.get_instance()
        self.item = item
        self.collection = self.parent().collection.get_collection(collection)
        # Obtain the object
        self.obj = self.collection.get(item)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)
        self.setupUi(item)

    def setupUi(self, item):
        super(Ui_Fitxa_Edit, self).setupUi(self)
        obj = self.obj
        schema = self.collection.schema
        # Topbar (title and icon)
        Topbar(widget=self.topbar, icon=schema.ico,
               title=schema.name.upper() + ' > ' + obj[schema.default])
        self._loadToolbar()

        self.fitxa_fields = {}
        for field in schema.order:
            value = field in obj and obj[field] or ''
            field_obj = schema.get_field(field)
            widgets = self.createField(field_obj, value)
            self.fitxa_fields[field] = widgets

    def createLabel(self, text, multiline=False):
        item = QtGui.QLabel(self)
        item.setText(text)
        item.setFont(self.fontLabel)
        if multiline:
            item.setAlignment(QtCore.Qt.AlignTop)
        return item

    def createField(self, field, value):
        columnspan = 1
        column = 0
        rowspan = 1
        itemLabel = self.createLabel(field.name, field.is_multivalue())
        self.fieldsLayout.addWidget(itemLabel, self.row, column,
                                    rowspan, columnspan)
        column += 1
        item = self.man.get_widget(field, self,
                               value, True)
        self.fieldsLayout.addWidget(item, self.row, column,
                                    rowspan, columnspan)
        self.row += 1
        return item

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
        params = self.parent().collector_uri_call(uri)
        if params is not None:
            action = params['action']
            if action == 'save':
                self.save()
            elif action == 'cancel':
                self.parent().display_view(
                    'fitxa',
                    {'item': self.item, 'collection': self.collection.get_id()})

    def save(self):
        schema = self.collection.schema
        data = {}
        for field in schema.order:
            widget = self.fitxa_fields[field]
            field_obj = schema.get_field(field)
            value = widget.text()
            if isinstance(value, QtCore.QString):
                value = str(value)
            data[field_obj.get_id()] = value
        data['id'] = self.obj['id']

        self.collection.save(data)
        self.parent().display_view(
            'fitxa',
            {'item': data['id'], 'collection': self.collection.get_id()})


class FitxaEditView(WidgetProvider):

    def getWidget(self, params):
        item = params['item']
        collection = params['collection']
        return Ui_Fitxa_Edit(item, collection, self.parent)
