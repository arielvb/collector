# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from collector.ui.gen.fitxa_edit import Ui_Form, _fromUtf8
from collector.ui.helpers.customtoolbar import CustomToolbar, Topbar
from collector.ui.widgetprovider import WidgetProvider
from collector.ui.helpers.fields import FieldWidgetManager


class Ui_Fitxa_New(QtGui.QWidget, Ui_Form):

    row = 0

    def __init__(self, collection, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Fitxa_New, self).__init__(parent, flags)
        self.man = FieldWidgetManager.get_instance()

        self.item = None
        self.collection = self.parent().collection.get_collection(collection)
        self.setupUi()

    def setupUi(self):
        super(Ui_Fitxa_New, self).setupUi(self)
        self._loadToolbar()
        # Obtain the object
        self.fontLabel = QtGui.QFont()
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)
        schema = self.collection.schema
        Topbar(widget=self.topbar, icon=schema.ico,
               title=schema.name.upper() + ' > ' + self.tr('New entry'))

        self.fitxa_fields = {}
        for field in schema.order:
            field_obj = schema.get_field(field)
            widgets = self.createField(field_obj, '')
            self.fitxa_fields[field] = widgets

    def createLabel(self, text, multiline=False):
        item = QtGui.QLabel(self)
        item.setFont(self.fontLabel)
        item.setText(text)
        item.setObjectName(_fromUtf8(text))
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
        if not isinstance(value, list):
            value = [value]
        widgets = []
        for i in value:
            item = self.man.get_widget(field, self,
                                   i, True)
            widgets.append(item)
            self.fieldsLayout.addWidget(item, self.row, column,
                                        rowspan, columnspan)
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
        params = self.parent().collector_uri_call(uri)
        action = params['action']
        if action == 'save':
            self.save()
        elif action == 'cancel':
            # TODO return to referer parameter?
            self.parent().display_view('collection',
                                      {'collection': self.collection.get_id()})

    def save(self):
        schema = self.collection.schema
        data = {}
        for field in schema.order:
            fields = self.fitxa_fields[field]
            value = None
            for widget in fields:
                value = widget.text()
                if isinstance(value, QtCore.QString):
                    value = str(value)
            data[field] = value
        from PyQt4.Qt import qDebug; qDebug(str(data))
        self.collection.save(data)
        self.parent().display_view('fitxa',
                                  {'item': data['id'],
                                  'collection': self.collection.get_id()})


class FitxaNewView(WidgetProvider):

    def get_widget(self, params):
        collection = params['collection']
        return Ui_Fitxa_New(collection, self.parent)
