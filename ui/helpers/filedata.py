# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

from ui.gen.file_data import Ui_Form
from ui.helpers.fields import FieldWidgetManager

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class FileDataWidget(QtGui.QWidget, Ui_Form):

    row = 0

    def __init__(self, schema, data, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(FileDataWidget, self).__init__(parent, flags)
        self.man = FieldWidgetManager.get_instance()
        self.schema = schema
        self.data = data
        self.fontLabel = QtGui.QFont()
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)
        self.setupUi()

    def createLabel(self, text, label=False):
        #item = QtGui.QLabel(self)
        item = self.man.get_widget('text', self, text)
        if label:
            item.setFont(self.fontLabel)
        return item

    def createField(self, field, value):
        columnspan = 1
        column = 0
        rowspan = 1
        itemLabel = self.createLabel(field.name, True)
        self.fieldsLayout.addWidget(itemLabel, self.row, column,
                                    rowspan, columnspan)
        column += 1
        if not isinstance(value, list):
            value = [value]
        for i in value:
            item = self.createLabel(i)
            self.fieldsLayout.addWidget(item, self.row, column,
                                        rowspan, columnspan)
            self.row += 1
        self.row += 1

    def setupUi(self):
        super(FileDataWidget, self).setupUi(self)

        obj = self.data
        schema = self.schema
        for field in schema.order:
            if field != 'image':
                value = field in obj and obj[field] or ''
                field_obj = schema.get_field(field)
                self.createField(field_obj, value)

        # TODO set image: we need to store it somewhere...
        #  but where is the best place?
        if 'image' in obj:
            src = obj['image']
            # TODO maybe set_value must be validate and get_value must
            #  translate the value
            image = schema.get_field('image')
            image.set_value(src)
            path = image.get_value()
            widget = self.man.get_widget('image', self, path)
            self.image_layout.addWidget(widget)
