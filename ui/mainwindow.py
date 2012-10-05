# -*- coding: utf-8 -*-
# pylint: disable-msg=E1101,W0403,E0611
# E0611: No name 'QtCore' in module 'PyQt4'
# E1101: Module 'PyQt4.QtCore' has no 'SIGNAL' member
# W0403: relative import
"""Collector main window"""
import logging
from PyQt4 import QtCore, QtGui
from gen.mainWindow import Ui_MainWindow
from views.dashboard import DashboardView
from views.fitxa_edit import FitxaEditView
from views.fitxa import FitxaView
from views.collection import CollectionView
from views.search import SearchView, DiscoverView, SearchDialog
from views.fitxa_new import FitxaNewView
from views.plugins import PluginsView
from views.properties import PropertiesView
from views.plugincollector_fitxa import PluginFileView
from views import ViewNotFound

from engine.collection import CollectionManager
from engine.plugin import PluginManager

try:
    _from_utf8 = QtCore.QString.fromUtf8
except AttributeError:
    _from_utf8 = lambda s: s


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """The Main Window of the UI"""

    was_maximized = False
    collection = None

    def __init__(self, parent=None):
        super(MainWindow,  self,).__init__(parent)
        self.plugin_manager = PluginManager.get_instance()

        self.collection = CollectionManager.get_instance()

        self.setupUi(self)
        self.setUnifiedTitleAndToolBarOnMac(True)
        # TODO clean toolbar code?
        # self.createToolbar()
        self.views = self.init_views()
        self.display_view('dashboard')
        # Menu actions
        self.help_menu = self.menuBar().addMenu("&Help")
        self.about_action = QtGui.QAction(
            "&About",
            self,
            statusTip="Show the application's About box",
            triggered=self.about)
        self.help_menu.addAction(self.about_action)
        # Connect menu actions
        QtCore.QObject.connect(
            self.actionView_Dashboard,
            QtCore.SIGNAL(_from_utf8("triggered()")),
            lambda: self.display_view('dashboard'))
        QtCore.QObject.connect(
            self.actionQuick_search,
            QtCore.SIGNAL(_from_utf8("triggered()")),
            lambda: self.display_view('quicksearch'))
        QtCore.QObject.connect(
            self.actionFullscreen,
            QtCore.SIGNAL(_from_utf8("triggered()")),
            self.switch_fullscreen)
        QtCore.QObject.connect(
            self.actionDiscover,
            QtCore.SIGNAL(_from_utf8("triggered()")),
            lambda: self.display_view('discover'))
        QtCore.QObject.connect(
            self.actionManage_plugins,
            QtCore.SIGNAL(_from_utf8("triggered()")),
            lambda: self.display_view('plugins'))
        QtCore.QObject.connect(
            self.actionProperties,
            QtCore.SIGNAL(_from_utf8("triggered()")),
            lambda: self.display_view('properties'))

    def init_views(self):
        """ Initialize the avaible views, each view is loaded by a provider"""
        return {
            'dashboard': DashboardView(self),
            'fitxa': FitxaView(self),
            'edit': FitxaEditView(self),
            'collection': CollectionView(self),
            'add': FitxaNewView(self),
            'search': SearchView(self),
            'discover': DiscoverView(self),
            'plugins': PluginsView(self),
            'quicksearch': SearchDialog(self),
            'properties': PropertiesView(self),
            'pluginfile': PluginFileView(self),
        }

    def display_view(self, name, params=None):
        """Launches the requested view by name with their parameters,
         if view doesn't exist throws an exception"""
        if not name in self.views:
            raise ViewNotFound('View "%s" not found' % name)
        if params is None:
            params = {}
        logging.debug("Called display view, URI:" +
                      self.viewcall2collectoruri(name, params))
        self.views[name].run(params)

    def switch_fullscreen(self):
        """Display fullscreen mode if isn't not active or shows the previous
        visualitzation maximized or normal window."""
        fullscreen = self.isFullScreen()
        if not fullscreen:
            self.was_maximized = False
            if self.isMaximized():
                self.was_maximized = True
            self.showFullScreen()
        else:
            if self.was_maximized:
                self.showMaximized()
            else:
                self.showNormal()

    def viewcall2collectoruri(self, view, params):
        """Transform a view plus params in a uri"""
        base = 'collector://view/' + view
        if params is not None:
            for param in params.items():
                base += '/' + param[0] + "/" + str(param[1])
        return base

    def collector_uri_call(self, uri):
        """Transforms an URI and launches the correct collector action."""
        # Prevent that uri aren't a string. if called from a signal the uri
        #  param will be a QString and doesn't have the startsWith method
        uri = str(uri)
        # Check protocol
        if not uri.startswith('collector://'):
            raise Exception("Not a collector uri")
        # Remove protocol
        uri = uri[len('collector://'):]
        params_encoded = uri.split('/')
        params = {}
        key = None
        for param in params_encoded:
            if key is None:
                key = param
            else:
                params[str(key)] = str(param)
                key = None
        if params_encoded[0] == 'view':
            self.display_view(params['view'], params)
        else:
            return params

    def about(self):
        """Creates the about window"""
        about_msg = _from_utf8("""collector |kəˈlektər|
noun a person or thing that collects something, in particular.
 - New Oxford dictionary

https://www.ariel.cat
                """)
        QtGui.QMessageBox.about(self, "About Collector", about_msg)
