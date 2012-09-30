# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.properties import Ui_Properties
from ui.gen.field_details import Ui_FieldDetails
from ui.widgetprovider import WidgetProvider
from ui.helpers.items import ObjectListItem


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class DetailsWidget(QtGui.QWidget, Ui_FieldDetails):

    def __init__(self, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(DetailsWidget, self).__init__(parent, flags)
        # self.collection = self.parent().collection.getName()
        self.setupUi(self)

    @QtCore.pyqtSlot(str, str, bool)
    def updateDetails(self, name, type, multivalue):
        self.detail_name.setText(name)
        self.detail_class.setText(type)
        # self.detail_value.hide()
        value = ''
        if multivalue:
            value = self.tr('True')
        else:
            value = self.tr('False')

        self.detail_value.setText(value)


class PropertiesWidget(QtGui.QDialog, Ui_Properties):
    """Properties widget"""

    def __init__(self, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(PropertiesWidget, self).__init__(parent, flags)
        # self.collection = self.parent().collection.getName()
        self.collection = self.parent().collection
        self.setupUi()

    def setupUi(self):
        super(PropertiesWidget, self).setupUi(self)
        # Title
        text = self.collection.get_title()
        self.title.setText(_fromUtf8(text))
        # Author
        text = self.collection.get_author()
        self.author.setText(_fromUtf8(text))
        # Description
        text = self.collection.get_description()
        self.description.setPlainText(_fromUtf8(text))
        # Persistence
        text = self.collection.get_persistence()
        self.persistence.setText(_fromUtf8(text))

        # Fields list
        font = QtGui.QFont()
        font.setBold(True)

        for collection in self.collection.collections.values():
            # Files
            c_name = collection.getName()
            list_item = QtGui.QListWidgetItem(c_name)
            self.last_entry_combo.addItem(c_name)
            self.new_entry_combo.addItem(c_name)
            icon = collection.schema.image
            if icon is None:
                icon = ':/folder.png'
            list_item.setIcon(QtGui.QIcon(_fromUtf8(icon)))
            list_item.setFont(font)
            self.fieldsList.addItem(list_item)
            # Fields
            for field_id in collection.schema.order:
                item = collection.schema.file.get(field_id)
                list_item = ObjectListItem(item, item.name)
                self.fieldsList.addItem(list_item)
        self.field_details = DetailsWidget(self)
        self.verticalLayout_3.addWidget(self.field_details)
        self.field_details.hide()

        # Buttons

        cancel = self.buttonBox.button(QtGui.QDialogButtonBox.Cancel)
        cancel.setDefault(True)

        # Connections
        QtCore.QObject.connect(
            self.buttonBox,
            QtCore.SIGNAL(_fromUtf8("accepted()")),
            lambda: self.save())

        QtCore.QObject.connect(
            self.buttonBox,
            QtCore.SIGNAL(_fromUtf8("rejected()")),
            lambda: self.reject())

        QtCore.QObject.connect(
            self.fieldsList,
            QtCore.SIGNAL("currentItemChanged(QListWidgetItem*, " +
                "QListWidgetItem*)"),
            self._itemSelected)

    def _itemSelected(self, item, old):
        if (getattr(item, 'obj', False)):
            # TODO multivalue detail
            self.field_details.updateDetails(
                item.obj.name,
                item.obj.get_pretty_type(),
                item.obj.is_multivalue())
            self.field_details.show()
        else:
            self.field_details.hide()

    def save(self):
        # TODO save method
        self.accept()


class PropertiesView(WidgetProvider):
    """Properties view"""

    mode = WidgetProvider.DIALOG_WIDGET

    def getWidget(self, params):
        # collection = params['collection']
        return PropertiesWidget(self.parent)
