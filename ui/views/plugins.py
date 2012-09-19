# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.plugins import Ui_Form

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class Ui_ManagePlugins(QtGui.QWidget, Ui_Form):

    def __init__(self, parent, flags=None):
        """ Creates a new dashboard view"""
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(Ui_ManagePlugins, self).__init__(parent, flags)
        self.setupUi()

    def setupUi(self):
        """Creates the ui elements for the dashboard.
        This function overrides the Ui_Form function creating thinks that
        aren't easy to do with the QT Designer"""
        super(Ui_ManagePlugins, self).setupUi(self)
        manager = self.parent().plugin_manager
        plugins = manager.plugins
        for plugin in manager.getEnabled():
            item = QtGui.QListWidgetItem()
            item.setText(plugins[plugin].get_name())
            self.listWidget.addItem(item)

        for plugin in manager.getDisabled():
            item = QtGui.QListWidgetItem()
            item.setText(plugin.get_name())
            self.listWidget_2.addItem(item)


class PluginsView():

    def __init__(self, parent):
        self.parent = parent

    def run(self, params={}):
        self.parent.fitxa = None
        w = Ui_ManagePlugins(self.parent)
        self.parent.setCentralWidget(w)
