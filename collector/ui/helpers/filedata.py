# -*- coding: utf-8 -*-
# pylint: disable-msg=E0611,E1101,C0103
"""
FileDataWidget
--------------
The layout for a file
"""
from PyQt4 import QtCore, QtGui

from collector.ui.gen.file_data import Ui_Form
from collector.ui.helpers.fields import FieldWidgetManager


class FileDataWidget(QtGui.QWidget, Ui_Form):
    """The widget that renders a file"""
    row = 0

    def __init__(self, schema, data, parent, flags=None):
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
        item.setWordWrap(True)
        item.setAlignment(QtCore.Qt.AlignLeading |
                          QtCore.Qt.AlignLeft |
                          QtCore.Qt.AlignTop)
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
        item = self.man.get_widget(field, self, value, False)
        self.fieldsLayout.addWidget(item, self.row, column,
                                    rowspan, columnspan)
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
                if field_obj.class_ == 'ref':
                    value = zip(value, obj.get(field, True))
                self.create_field(field_obj, value)
        if 'image' in obj:
            src = obj['image']
            image = schema.get_field('image')
            image.set_value(src)
            path = image.get_value()
            widget = self.man.get_widget(image, self, {
                'src': path,
                'x': self.parent().width() / 2,
                'y': self.parent().height() - 200})
            self.image_layout.addWidget(widget)
        else:
            self.line.hide()
        # if len(obj) < 3:
        #     self.line.hide()
