# -*- coding: utf-8 -*-

# TODO all the widgets for all the fields
from PyQt4 import QtGui, QtCore
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

from ui.gen.file_selector import Ui_FileSelector

from abc import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class FieldWidget:

    __metaclass__ = ABCMeta

    @abstractmethod
    def prepareWidget(self, parent, value):
        """Preperes a new widget in edit mode"""

    @abstractmethod
    def prepareWidgetEdit(cls, parent, value):
        """Preperes a new widget in edit mode"""

    def getWidget(self, parent, value):
        return self.prepareWidget(parent, value)

    def getWidgetEdit(self, parent, value):
        return self.prepareWidgetEdit(parent, value)


class FieldTextWidget(FieldWidget):

    def prepareWidget(self, parent, value):
        widget = QtGui.QLabel(parent)
        widget.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse |
                                   QtCore.Qt.TextSelectableByMouse)
        try:
            if isinstance(value, int):
                value = str(value)
            widget.setText(_fromUtf8(value))
        except Exception:
            widget.setText("Error")
        return widget

    def prepareWidgetEdit(self, parent, value):
        widget = QtGui.QLineEdit(parent)
        try:
            # TODO custom widget for Int values
            if isinstance(value, int):
                value = str(value)
            widget.setText(_fromUtf8(value))
        except Exception:
            widget.setText("Error")
        return widget
        # w.setObjectName(_fromUtf8(text))


class ImageWidget(QtGui.QLabel):

    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.nam = QNetworkAccessManager()

    def set_image(self, value, max_x, max_y):
        pixmap = None
        if value != '':
            pixmap = QtGui.QPixmap(value)
        # Check if the file doensn't have image or the image file
        #  doesn't exists
        if pixmap is None or pixmap.isNull():
            pixmap = QtGui.QPixmap(_fromUtf8(':box.png'))
        if value.startswith('http'):
            logging.debug('FILEDATA loading image from url %s', value)
            self.nam.finished.connect(lambda r: self.image_complete(r))
            self.nam.get(QNetworkRequest(QtCore.QUrl(value)))
        scaled = pixmap.scaled(max_x, max_y, QtCore.Qt.KeepAspectRatio)
        self.setPixmap(scaled)
        self.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft |
                          QtCore.Qt.AlignTop)

    def image_complete(self, reply):
        img = QtGui.QImage()
        img.loadFromData(reply.readAll())
        pixmap = QtGui.QPixmap(img)
        scaled = pixmap.scaled(250, 250, QtCore.Qt.KeepAspectRatio)
        self.setPixmap(scaled)


class FileSelector(QtGui.QWidget, Ui_FileSelector):
    """A file selector implementation"""

    def __init__(self, parent=None, filter_=None):
        super(FileSelector, self).__init__(parent)
        self.filter = filter_
        self.setupUi(self)
        self.connect(
            self.dialog,
            QtCore.SIGNAL(_fromUtf8("clicked()")),
            lambda: self.open_dialog())

    def setText(self, text):
        """Sets the path for the file"""
        #TODO this is a slot
        self.path.setText(text)

    def text(self):
        return self.path.text()

    def open_dialog(self, filter=None):
        file_name = QtGui.QFileDialog.getOpenFileName(self,
                "Choose file",
                self.path.text(),
                self.filter)
        self.setText(file_name)


class FieldImageWidget(FieldWidget):

    def prepareWidget(self, parent, value):
        widget = ImageWidget(parent)
        widget.set_image(value, 250, 250)
        return widget

    def prepareWidgetEdit(self, parent, value):
        #TODO this widget must be a file selector
        widget = FileSelector(parent, 'Images (*.jpg *.png)')
        widget.setText(value)
        return widget


class FieldWidgetManager(object):

    register = {}
    _instance = None

    def __init__(self):
        if FieldWidgetManager._instance is not None:
            raise Exception("Called more that once")
        FieldWidgetManager._instance = self
        self.default = FieldTextWidget()
        self.register['text'] = self.default
        self.register['image'] = FieldImageWidget()

    @staticmethod
    def get_instance():
        if FieldWidgetManager._instance is None:
            FieldWidgetManager._instance = FieldWidgetManager()
        return FieldWidgetManager._instance

    def get(self, id_):
        return self.register[id_]

    def get_widget(self, id_, parent, value, edit=False):
        provider = self.default
        if id_ in self.register:
            provider = self.register[id_]
        widget = None
        if not edit:
            widget = provider.getWidget(parent, value)
        else:
            widget = provider.getWidgetEdit(parent, value)
        return widget

    def add(self, id, field):
        self.register[id] = field


def main():
    manager = FieldWidgetManager()

if __name__ == '__main__':
    main()
