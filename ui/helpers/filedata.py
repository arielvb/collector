# -*- coding: utf-8 -*-
# pylint: disable-msg=E0611,E1101,C0103
"""
FileDataWidget
--------------
The layout for a file
"""
from PyQt4 import QtCore, QtGui

from ui.gen.file_data import Ui_Form
from ui.helpers.fields import FieldWidgetManager


class FileDataWidget(QtGui.QWidget, Ui_Form):
    """The widget that renders a file"""
    row = 0

    def __init__(self, schema, data, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(FileDataWidget, self).__init__(parent, flags)
        self.man = FieldWidgetManager.get_instance()
        self.schema = schema
        self.data = data
        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setWeight(75)
        self.setupUi(self)

    def create_label(self, text):
        """Creates a widget label, is used to display the field name"""
        item = QtGui.QLabel(self)
        item.setText(text)
        item.setFont(self.font)
        return item

    def create_field(self, field, value):
        """Creates the widget who renders the received *field* and displays
         the received value"""
        columnspan = 1
        column = 0
        rowspan = 1
        # The label
        item = self.create_label(field.name)
        self.fieldsLayout.addWidget(item, self.row, column,
                                    rowspan, columnspan)
        column += 1
        # The widget
        if not isinstance(value, list):
            value = [value]
        for i in value:
            item = self.man.get_widget(field, self,
                                   i, False)
            self.fieldsLayout.addWidget(item, self.row, column,
                                        rowspan, columnspan)
            self.row += 1
        self.row += 1

    def setupUi(self, form):
        """Renders all the widget ui"""
        super(FileDataWidget, self).setupUi(form)

        obj = self.data
        schema = self.schema
        for field in schema.order:
            if field != 'image':
                value = field in obj and obj[field] or ''
                field_obj = schema.get_field(field)
                self.create_field(field_obj, value)

        if 'image' in obj:
            src = obj['image']
            image = schema.get_field('image')
            image.set_value(src)
            path = image.get_value()
            widget = self.man.get_widget(image, self, path)
            self.image_layout.addWidget(widget)

        if len(obj) < 3:
            self.line.hide()
