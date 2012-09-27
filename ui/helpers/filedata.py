# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

from ui.gen.file_data import Ui_Form

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
        self.schema = schema
        self.data = data
        self.setupUi()

    def createLabel(self, text, label=False):
        item = QtGui.QLabel(self)
        if label:
            item.setFont(self.fontLabel)
        else:
            item.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse |
                                         QtCore.Qt.TextSelectableByMouse)
        #TODO deal whit encoding
        try:
            if isinstance(text, int):
                text = str(text)
            item.setText(_fromUtf8(text))
        except Exception:
            item.setText("Error")

        # item.setObjectName(_fromUtf8(str(text)))
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

    def image_complete(self, reply):
        img = QtGui.QImage()
        img.loadFromData(reply.readAll())
        pixmap = QtGui.QPixmap(img)
        scaled = pixmap.scaled(250, 250, QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(scaled)

    def setupUi(self):
        super(FileDataWidget, self).setupUi(self)

        self.fontLabel = QtGui.QFont()
        self.fontLabel.setBold(True)
        self.fontLabel.setWeight(75)
        obj = self.data
        schema = self.schema
        for field in schema.order:
            if field != 'image':
                value = field in obj and obj[field] or ''
                self.createField(schema.fields[field]['name'], value)

        # TODO set image: we need to store it somewhere...
        #  but where is the best place?
        if 'image' in obj:
            from PyQt4.Qt import qDebug; qDebug(obj['image'])
            image = schema.get_field('image')
            image.set_value(obj['image'])
            path = image.get_value()
            pixmap = None
            if path != '':
                pixmap = QtGui.QPixmap(path)
            # Check if the file doensn't have image or the image file
            #  doesn't exists
            if pixmap is None or pixmap.isNull():
                pixmap = QtGui.QPixmap(_fromUtf8(':box.png'))
            if obj['image'].startswith('http'):
                self.nam = QNetworkAccessManager()
                self.nam.finished.connect(lambda r: self.image_complete(r))
                self.nam.get(QNetworkRequest(QtCore.QUrl(obj['image'])))
            scaled = pixmap.scaled(250, 250, QtCore.Qt.KeepAspectRatio)
            self.image.setPixmap(scaled)
        else:
            self.image.hide()
