# -*- coding: utf-8 -*-

# TODO refractor this file must contain for each field:
#  (provider, widget)
from PyQt4 import QtGui, QtCore
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
from engine.collection import CollectionManager
from ui.gen.file_selector import Ui_FileSelector
from ui.gen.widget_ref import Ui_Reference


from abc import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class FieldWidget:

    __metaclass__ = ABCMeta

    @abstractmethod
    def prepareWidget(self, parent, field, value):
        """Preperes a new widget in edit mode"""

    @abstractmethod
    def prepareWidgetEdit(cls, parent, field, value):
        """Preperes a new widget in edit mode"""

    def getWidget(self, parent, field, value):
        return self.prepareWidget(parent, field, value)

    def getWidgetEdit(self, parent, field, value):
        return self.prepareWidgetEdit(parent, field, value)


class FieldTextWidget(FieldWidget):

    def prepareWidget(self, parent, field, value):
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

    def prepareWidgetEdit(self, parent, field, value):
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

    def prepareWidget(self, parent, field, value):
        widget = ImageWidget(parent)
        widget.set_image(value, 250, 250)
        return widget

    def prepareWidgetEdit(self, parent, field, value):
        #TODO this widget must be a file selector
        widget = FileSelector(parent, 'Images (*.jpg *.png)')
        widget.setText(value)
        return widget


class ReferenceWidget(QtGui.QWidget, Ui_Reference):
    """ReferenceWidget, the edit widget for reference fields"""

    def __init__(self, field, value, parent=None):
        super(ReferenceWidget, self).__init__(parent)
        self.man = CollectionManager.get_instance()
        self.field = field
        self.setupUi(self)
        self.values = []
        self.reload(value)

    def text(self):
        currentIndex = self.comboBox.currentIndex()
        value = ''
        if currentIndex > 0:
            id_ = self.values[currentIndex].id
            value = id_
            return int(value)
        return ''

    def reload(self, value):
        """Reloads the content of the widget"""
        collection_id = self.field.ref_collection
        dst_field = self.field.ref_field
        dst_collection = self.man.get_collection(collection_id)
        contents = dst_collection.get_all()
        self.comboBox.clear()
        self.values.append('')
        self.comboBox.addItem('')
        # TODO maybe is more eficinet use QStringList
        i = 1
        for reference in contents:
            # TODO we need to store the object, because if the field is empty??
            # or whe must make the field required in the dst collection?
            self.values.append(reference)
            item = reference[dst_field]
            self.comboBox.addItem(item)
            if reference['id'] == value:
                self.comboBox.setCurrentIndex(i)
            i += 1


class FiedlReferenceWidget(FieldTextWidget):

    def prepareWidgetEdit(self, parent, field, value):
        #TODO this widget must be a file selector
        widget = ReferenceWidget(field, value, parent)
        return widget


class IntWidget(QtGui.QSpinBox):

    def __init__(self, parent=None):
        super(IntWidget, self).__init__(parent)
        self.setMaximum(9999)
        self.setMinimum(-9999)

    def setValue(self, value):
        if isinstance(value, (str, unicode)):
            if value == '':
                value = 0
            value = int(value)
        super(IntWidget, self).setValue(value)

    def text(self):
        value = int(super(IntWidget, self).text())
        return value


class FieldIntWidget(FieldTextWidget):

    def prepareWidgetEdit(self, parent, field, value):
        #TODO this widget must be a file selector
        w = IntWidget(parent)
        w.setValue(value)
        return w


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
        self.register['ref'] = FiedlReferenceWidget()
        self.register['int'] = FieldIntWidget()

    @staticmethod
    def get_instance():
        if FieldWidgetManager._instance is None:
            FieldWidgetManager._instance = FieldWidgetManager()
        return FieldWidgetManager._instance

    def get(self, id_):
        return self.register[id_]

    def get_widget(self, field, parent, value, edit=False):
        provider = self.default
        id_ = field.class_
        if id_ in self.register:
            provider = self.register[id_]
        widget = None
        if not edit:
            widget = provider.getWidget(parent, field, value)
        else:
            widget = provider.getWidgetEdit(parent, field, value)
        return widget

    def add(self, field_type, widget_provider):
        self.register[field_type] = widget_provider


def main():
    manager = FieldWidgetManager()

if __name__ == '__main__':
    main()
