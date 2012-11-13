# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.preferences import Ui_PreferencesDialog, _fromUtf8
from ui.widgetprovider import WidgetProvider
from ui.helpers.items import ObjectListItem
from engine.collector import Collector


class Ui_Preferences(QtGui.QDialog, Ui_PreferencesDialog):

    def __init__(self, parent, flags=None):
        """ Creates a new dialog to render the application preferences"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_Preferences, self).__init__(parent, flags)
        self.manager = Collector.get_instance().get_manager("plugin")
        self.current_lang = None
        self.codes = ['ca_ES', 'en_UK', 'es_ES']
        self.setupUi()

    def setupUi(self):
        """Creates the ui elements for the preferences.
        This function overrides the Ui_Form function creating thinks that
        aren't easy to do with the QT Designer"""
        super(Ui_Preferences, self).setupUi(self)
        self.refresh()
        self.connect(self.buttonBox,
            QtCore.SIGNAL(_fromUtf8("accepted()")), self.saveandclose)

        self.connect(
            self.b_disable,
            QtCore.SIGNAL(_fromUtf8("clicked()")), self.disable)
        self.connect(
            self.b_enable,
            QtCore.SIGNAL(_fromUtf8("clicked()")), self.enable)
        # Language selector
        self.current_lang = Collector.get_instance().conf('lang')
        if not self.current_lang is None:
            index = 1
            try:
                index = self.codes.index(str(self.current_lang))
            except ValueError:
                index = 1
            self.lang_combo.setCurrentIndex(index)


    @QtCore.pyqtSlot()
    def disable(self):
        """Disable selecte plugins"""
        selected = self.listWidget.selectedItems()
        to_disable = []
        for item in selected:
            to_disable.append(item.obj.get_id())
        self.manager.disable(to_disable)
        self.manager.save()
        self.refresh()

    @QtCore.pyqtSlot()
    def enable(self):
        """Enables selected plugins"""
        selected = self.listWidget_2.selectedItems()
        to_enable = []
        for item in selected:
            to_enable.append(item.obj.get_id())
        self.manager.enable(to_enable)
        self.manager.save()
        self.refresh()

    def refresh(self):
        """Refreshes the content of the lists"""
        self.listWidget.clear()
        self.listWidget_2.clear()

        for plugin in self.manager.get_enabled():
            obj = self.manager.get(plugin)
            item = ObjectListItem(obj, obj.get_name())
            item.setIcon(QtGui.QIcon(_fromUtf8(obj.icon)))
            self.listWidget.addItem(item)

        for plugin in self.manager.get_disabled():
            obj = self.manager.get(plugin)
            item = ObjectListItem(obj, obj.get_name())
            item.setIcon(QtGui.QIcon(_fromUtf8(obj.icon)))
            self.listWidget_2.addItem(item)

    def saveandclose(self):
        """Saves unsaved data and closes"""
        config = Collector.get_instance().get_manager('config')
        config.set('lang', self.codes[self.lang_combo.currentIndex()])
        config.save()
        self.close()


class PreferencesView(WidgetProvider):

    mode = WidgetProvider.DIALOG_WIDGET

    def get_widget(self, params):
        return Ui_Preferences(self.parent)
