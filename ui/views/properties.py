# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.properties import Ui_Properties, _fromUtf8
from ui.gen.field_details import Ui_FieldDetails
from ui.widgetprovider import WidgetProvider
from ui.helpers.items import ObjectListItem
from ui.views.dashboard import Ui_Dashboard


class DetailsWidget(QtGui.QWidget, Ui_FieldDetails):

    def __init__(self, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(DetailsWidget, self).__init__(parent, flags)
        # self.collection = self.parent().collection.get_id()
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
        # self.collection = self.parent().collection.get_id()
        self.collection = self.parent().collection
        self.setupUi()

    def setupUi(self):
        super(PropertiesWidget, self).setupUi(self)
        # Info tab {
        info = self.collection.get_properties()
        # > Title
        self.title.setText(_fromUtf8(info['name']))
        # > Author
        self.author.setText(_fromUtf8(info['author']))
        # > Description
        self.description.setPlainText(_fromUtf8(info['description']))
        # > Persistence
        text = self.collection.get_persistence()
        self.persistence.setText(_fromUtf8(text))
        # } End info tab
        # Fields list
        font = QtGui.QFont()
        font.setBold(True)

        for collection in self.collection.collections.values():
            # Files
            c_name = collection.get_name()
            id_ = collection.get_id()
            list_item = QtGui.QListWidgetItem(c_name)
            self.search_combo.addItem(c_name, id_)
            self.last_entry_combo.addItem(c_name, id_)
            self.new_entry_combo.addItem(c_name, id_)
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
        self.details_layout.addWidget(self.field_details)
        self.field_details.hide()
        preview = Ui_Dashboard(self.parent())
        preview.setDisabled(True)
        self.preview_layout.addWidget(preview)

        # Buttons

        cancel = self.buttonBox.button(QtGui.QDialogButtonBox.Cancel)
        cancel.setDefault(True)

        # Connections
        self.connect(
            self.buttonBox,
            QtCore.SIGNAL(_fromUtf8("accepted()")),
            self.save
        )

        self.connect(
            self.buttonBox,
            QtCore.SIGNAL(_fromUtf8("rejected()")),
            self.reject
        )

        self.connect(
            self.fieldsList,
            QtCore.SIGNAL("currentItemChanged(QListWidgetItem*, " +
                "QListWidgetItem*)"),
            self._itemSelected
        )

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
        """Stores the properties"""
        # Info tab
        valid = True
        info = {
            'name': unicode(self.title.text().toUtf8()),
            'author': unicode(self.author.text().toUtf8()),
            'description': unicode(self.description.toPlainText().toUtf8())
        }
        #Dashboard tab
        dashboard = {
            'lastcollection': unicode(self.last_entry_combo.itemData(
                self.last_entry_combo.currentIndex()).toUtf8()),
            'newbutton': unicode(self.new_entry_combo.itemData(
                self.new_entry_combo.currentIndex()).toUtf8()),
            'quicksearch': unicode(self.search_combo.itemData(
                self.search_combo.currentIndex()).toUtf8()),
        }
        info['dashboard'] = dashboard
        # TODO save all the tabs: files, plugins
        self.collection.set_properties(info)
        if valid:
            if self.parent().view == 'dashboard':
                self.parent().centralWidget().reload()
            self.accept()


class PropertiesView(WidgetProvider):
    """Properties view"""

    mode = WidgetProvider.DIALOG_WIDGET

    def get_widget(self, params):
        # collection = params['collection']
        return PropertiesWidget(self.parent)
