# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.plugins import Ui_PluginDialog, _fromUtf8
from ui.widgetprovider import WidgetProvider
from ui.helpers.items import ObjectListItem
from engine.collector import Collector


class Ui_ManagePlugins(QtGui.QDialog, Ui_PluginDialog):

    def __init__(self, parent, flags=None):
        """ Creates a new dashboard view"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_ManagePlugins, self).__init__(parent, flags)
        self.manager = Collector.get_instance().get_manager("plugin")

        self.setupUi()

    def setupUi(self):
        """Creates the ui elements for the dashboard.
        This function overrides the Ui_Form function creating thinks that
        aren't easy to do with the QT Designer"""
        super(Ui_ManagePlugins, self).setupUi(self)
        self.refresh()
        self.connect(
            self.b_disable,
            QtCore.SIGNAL(_fromUtf8("clicked()")), self.disable)
        self.connect(
            self.b_enable,
            QtCore.SIGNAL(_fromUtf8("clicked()")), self.enable)


    @QtCore.pyqtSlot()
    def disable(self):
        selected = self.listWidget.selectedItems()
        to_disable = []
        for item in selected:
            to_disable.append(item.obj.get_id())
        self.manager.disable(to_disable)
        self.manager.save()
        self.refresh()

    @QtCore.pyqtSlot()
    def enable(self):
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
            self.listWidget.addItem(item)

        for plugin in self.manager.get_disabled():
            obj = self.manager.get(plugin)
            item = ObjectListItem(obj, obj.get_name())
            self.listWidget_2.addItem(item)



class PluginsView(WidgetProvider):

    mode = WidgetProvider.DIALOG_WIDGET

    def getWidget(self, params):
        return Ui_ManagePlugins(self.parent)
