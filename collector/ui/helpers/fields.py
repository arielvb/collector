# -*- coding: utf-8 -*-
"""
Fields - Widgets and providers
==============================

This module is formed by the basic fields supported by Collector. For every
 field a edit widget and a reaonly widget are defiened.

The access to a widget a manager has been defiened, the FieldWidgetManager,
 that has a registry of every existing widget and allows create new instances
 of each one in both modes (readlony, write).
"""
from abc import ABCMeta, abstractmethod
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot, Qt, SIGNAL, QUrl
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt4.QtNetwork import QNetworkReply
from collector.core.collection import Collection
from collector.ui.gen.file_selector import Ui_FileSelector, _fromUtf8
from collector.ui.gen.widget_ref import Ui_Reference
from collector.ui.gen.widget_multivalue import Ui_Multivalue
import logging


class FieldWidget(object):
    """The base class for a widget providers"""

    __metaclass__ = ABCMeta

    @abstractmethod
    def prepare(self, parent, field, value):
        """Preperes a new widget in edit mode"""

    @abstractmethod
    def prepare_edit(self, parent, field, value):
        """Preperes a new widget in edit mode"""

    def getWidget(self, parent, field, value):
        """Creates a new widget for the field in readonly mode"""
        return self.prepare(parent, field, value)

    def getWidgetEdit(self, parent, field, value):
        """Creates a new widget for the field in edit mode"""
        return self.prepare_edit(parent, field, value)


class TextWidget(QtGui.QLineEdit):
    """TextWidget, overrides QLineEdit to add the get_value method"""

    get_value = lambda self: unicode(self.text().toUtf8(), 'utf-8')


class FieldTextWidget(FieldWidget):
    """Provides a field text widget"""

    def prepare(self, parent, field, value):
        widget = QtGui.QLabel(parent)
        widget.setTextInteractionFlags(Qt.LinksAccessibleByMouse |
                                       Qt.TextSelectableByMouse)
        try:
            if not isinstance(value, (str, unicode)):
                value = unicode(value)
            widget.setText(_fromUtf8(value))
        except Exception:
            widget.setText("Error")
        return widget

    def prepare_edit(self, parent, field, value):
        widget = TextWidget(parent)
        try:
            if value is None:
                value = ''
            if not isinstance(value, (str, unicode)):
                value = unicode(value)
            widget.setText(_fromUtf8(value))
        except Exception:
            widget.setText("Error")
        return widget


class ImageWidget(QtGui.QLabel):
    """ImageWidget extends QLabel adding the special method set_image,
    who allows load images from disk or network"""

    default_src = ':box.png'

    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.http_image_complete)
        self.src = ''
        self.max_x = None
        self.max_y = None

    def set_image(self, value, max_x=450, max_y=450):
        """Changes the current image to the new one, and resizes the widget
         if the size is different."""
        self.max_x = max_x
        self.max_y = max_y
        pixmap = None
        if value is None or value == '':
            value = self.default_src
        if value.startswith('http'):
            logging.debug('FILEDATA loading image from url %s', value)
            self.nam.get(QNetworkRequest(QUrl(value)))
        else:
            pixmap = QtGui.QPixmap(value)
            if pixmap.isNull():
                pixmap = QtGui.QPixmap(_fromUtf8(self.default_src))
            scaled = pixmap.scaled(max_x, max_y, Qt.KeepAspectRatio)
            self.setPixmap(scaled)
        self.setAlignment(Qt.AlignLeading | Qt.AlignLeft |
                          Qt.AlignTop)
        self.src = value

    def http_image_complete(self, reply):
        """This function is called when the image has been loadded from the
         network"""
        pixmap = None
        if reply.error() == QNetworkReply.NoError:
            img = QtGui.QImage()
            img.loadFromData(reply.readAll())
            pixmap = QtGui.QPixmap(img)
        else:
            logging.info("NETWORK failed to obtain image %s:",
                         reply.errorString())
            pixmap = QtGui.QPixmap(_fromUtf8(self.default_src))
        if self.max_x is not None and self.max_y is not None:
            scaled = pixmap.scaled(self.max_x, self.max_y, Qt.KeepAspectRatio)
            del pixmap
            pixmap = scaled
        self.setPixmap(pixmap)

    def __del__(self):
        self.nam.finished.disconnect()


class FileSelector(QtGui.QWidget, Ui_FileSelector):
    """A file selector implementation"""

    def __init__(self, parent=None, filter_=None):
        super(FileSelector, self).__init__(parent)
        self.filter = filter_
        self.setupUi(self)
        self.connect(
            self.dialog,
            SIGNAL(_fromUtf8("clicked()")),
            self.open_dialog
        )

    @pyqtSlot()
    def set_value(self, text):
        """Sets the path for the file"""
        self.path.setText(text)

    def get_value(self):
        """Returns the value of the field"""
        return self.path.text()

    text = get_value

    @pyqtSlot()
    def open_dialog(self):
        """Opens the file selector dialog"""
        file_name = QtGui.QFileDialog.getOpenFileName(
            self,
            "Choose file",
            self.path.text(),
            self.filter)
        self.set_value(file_name)


class FieldImageWidget(FieldWidget):
    """Provider for ImageWidgets"""

    def prepare(self, parent, field, value):
        """
        Creates a new ImageWidget.
        The value of the widget *value* can be a dictionary
        with the keys:
            src   path to the image
            x     max x image size
            y     max y image size
        Or a string, that will be the path of the image.
        """
        widget = ImageWidget(parent)
        if isinstance(value, str):
            widget.set_image(value, 450, 450)
        elif isinstance(value, dict):
            widget.set_image(value['src'], value['x'], value['y'])
        else:
            raise ValueError()
        return widget

    def prepare_edit(self, parent, field, value):
        #TODO this widget must be a file selector
        widget = FileSelector(parent, 'Images (*.jpg *.png)')
        widget.set_value(value)
        return widget


class ReferenceWidget(QtGui.QWidget, Ui_Reference):
    """ReferenceWidget, the edit widget for reference fields"""

    def __init__(self, field, value, parent=None):
        super(ReferenceWidget, self).__init__(parent)
        self.man = Collection.get_instance()
        self.field = field
        self.setupUi(self)
        self.addValue.hide()
        self.values = []
        self.reload(value)

    def get_value(self):
        currentIndex = self.comboBox.currentIndex()
        value = ''
        if currentIndex > 0:
            id_ = self.values[currentIndex].id
            value = id_
            return int(value)
        return ''
    #TODO remove shortcut
    text = get_value

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

    def prepare_edit(self, parent, field, value):
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

    def get_value(self):
        value = int(super(IntWidget, self).text())
        return value

    # TODO remove this shortcut
    text = get_value


class FieldIntWidget(FieldTextWidget):

    def prepare_edit(self, parent, field, value):
        w = IntWidget(parent)
        if value is not None:
            w.setValue(value)
        return w


class MultivalueWidget(QtGui.QWidget, Ui_Multivalue):

    def __init__(self, widgetprovider, parent, field, values):
        super(MultivalueWidget, self).__init__(parent)
        self.widgetprovider = widgetprovider
        self.setupUi(self)
        self.widgets = []
        self.field = field
        i = 0
        for value in values:
            i += 1
            self.add_value(value)
        if i == 0:
            self.add_value()

        self.connect(
            self.addValue,
            SIGNAL(_fromUtf8("clicked()")),
            self.add_value)

    def add_value(self, default=None):
        widget = self.widgetprovider.getWidgetEdit(self, self.field, default)
        self.fields.addWidget(widget)
        self.widgets.append(widget)

    def get_values(self):
        values = []
        for widget in self.widgets:
            if widget.get_value() is not None:
                values.append(widget.get_value())
        return values

    text = get_values


class FieldWidgetManager(object):
    """The field provider manager"""

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
        """Obtains the manager instance"""
        if FieldWidgetManager._instance is None:
            FieldWidgetManager._instance = FieldWidgetManager()
        return FieldWidgetManager._instance

    def get(self, id_):
        """Obtains a widget provider by id"""
        return self.register[id_]

    def get_widget(self, field, parent, value, edit=False):
        """Returns the widget associated to the field in
         readonly or edit mode."""
        provider = self.default
        id_ = field.class_
        if id_ in self.register:
            provider = self.register[id_]
        widget = None
        if not edit:
            widget = provider.getWidget(parent, field, value)
        else:
            if field.is_multivalue():
                widget = MultivalueWidget(provider, parent, field, value)
            else:
                widget = provider.getWidgetEdit(parent, field, value)
        return widget

    def add(self, field_type, widget_provider):
        """Registers a provider for the defeined field_type, overriding any
         previous definition."""
        self.register[field_type] = widget_provider
