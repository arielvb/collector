# -* coding: utf-8 *-
from PyQt4 import QtGui
from ui.gen.im_export import Ui_Dialog
from ui.widgetprovider import WidgetProvider
from ui.helpers.customtoolbar import CustomToolbar
from engine.collector import get_manager
from engine.plugin import PluginExporter, PluginImporter
import logging


class BaseDialog(QtGui.QDialog, Ui_Dialog):
    """
    BaseDialog
    ----------
    Common parts for ImportDialog and ExportDialog
    """

    def __init__(self, parent=None):
        super(BaseDialog, self).__init__(parent)
        self.setupUi(self)
        self.customize()

    def customize(self):
        self.label_noplugins.hide()
        plugins = self.get_plugins()
        man = get_manager('plugin')
        items = []
        for i in plugins:
            plugin = man.get(i)
            items.append(
                {'class': 'link', 'name': plugin.get_name(),
             'path': 'plugin/' + plugin.get_id(),
             'image': plugin.icon()}
            )

        # Toolbar
        items.append({'class': 'spacer'})
        CustomToolbar(self.toolbar, items, self.select_plugin)
        if not len(plugins):
            self.toolbar.hide()
            self.label_noplugins.show()

    def select_plugin(self, uri):
        """Select plugin callback"""
        params = self.parent().collector_uri_call(uri)
        if params is not None:
            plugin = params.get('plugin', None)
            if plugin is not None:
                man = get_manager('plugin')
                self.hide()
                try:
                    man.get(plugin).run()
                    self.done(1)
                except Exception as exc:
                    logging.exception(exc)
                    self.done(-1)

    def get_plugins(self):
        plugins = get_manager('plugin').filter(self.filter_)
        return plugins


class ExportDialog(BaseDialog):
    """
    ExportDialog
    ------------
    """
    # TODO

    filter_ = PluginExporter

    def customize(self):
        super(ExportDialog, self).customize()
        self.setWindowTitle(self.tr("Export"))


class ImportDialog(BaseDialog):
    """
    ImportDialog
    ------------
    """
    filter_ = PluginImporter

    def customize(self):
        super(ImportDialog, self).customize()
        self.setWindowTitle(self.tr("Import"))


class ImportView(WidgetProvider):
    """Properties view"""

    mode = WidgetProvider.DIALOG_WIDGET

    def get_widget(self, params):
        return ImportDialog(self.parent)


class ExportView(WidgetProvider):
    """Properties view"""

    mode = WidgetProvider.DIALOG_WIDGET

    def get_widget(self, params):
        return ExportDialog(self.parent)
