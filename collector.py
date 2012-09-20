#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# pylint: disable-msg=E1101,W0403,E0611
# E0611: No name 'QtCore' in module 'PyQt4'
# E1101: Module 'PyQt4.QtCore' has no 'SIGNAL' member
# W0403: relative import
"""Collector main script"""
# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui
from ui.gen.mainWindow import Ui_MainWindow
from ui.views.dashboard import DashboardView
from ui.views.fitxa_edit import FitxaEditView
from ui.views.fitxa import FitxaView
from ui.views.collection import CollectionView
from ui.views.search import SearchView, DiscoverView, SearchDialog
from ui.views.fitxa_new import FitxaNewView
from ui.views.plugins import PluginsView
from ui.views.properties import PropertiesView

from engine.collection import CollectionManager
from engine.plugin import PluginManager
from engine.config import Config
from plugins.boardgamegeek import PluginBoardGameGeek

import sys
import os

try:
    _from_utf8 = QtCore.QString.fromUtf8
except AttributeError:
    _from_utf8 = lambda s: s


class ViewNotFound(Exception):
    """Custom exception raised when a view is requested and doesn't exists"""


class CollectorUI(QtGui.QMainWindow, Ui_MainWindow):
    """The Main Window of the UI"""

    was_maximized = False
    collection = None

    def __init__(self, parent=None):
        super(CollectorUI,  self,).__init__(parent)
        config = Config.getInstance()
        config.build_data_directory()
        sys_plugin_path = config.get_appdata_path()
        sys_plugin_path = os.path.join(sys_plugin_path, 'user_plugins')

        self.plugin_manager = PluginManager(
            ['PluginHellouser', 'PluginBoardgamegeek'],
            {'PluginBoardgamegeek': PluginBoardGameGeek()},
            paths=[sys_plugin_path])

        self.collection = CollectionManager.getInstance()

        self.setupUi(self)
        self.setUnifiedTitleAndToolBarOnMac(False)
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
            'properties': PropertiesView(self)
        }

    def display_view(self, name, params={}):
        """Launches the requested view by name with their parameters,
         if view doesn't exist throws an exception"""
        if not name in self.views:
            raise ViewNotFound('View "%s" not found' % name)
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


class SplashScreen(object):
    """Displays a splash screen until the main window is ready"""

    def __init__(self):
        splash_pix = QtGui.QPixmap('./data/collector_splash.png')
        self.splash = QtGui.QSplashScreen(splash_pix,
                                          QtCore.Qt.WindowStaysOnTopHint)
        self.splash.setMask(splash_pix.mask())

    def show(self):
        """Displays the splash screen"""
        self.splash.show()
        import time
        # ensure at least its visible one second
        time.sleep(1)

    def finish(self, window):
        """Hides and destroy the splash screen, ensure the """
        self.splash.finish(window)


class CollectorApplication(QtGui.QApplication):
    """The GUI Aplication for Collector"""

    translators = {}
    current = None

    def __init__(self, argv):
        super(CollectorApplication, self).__init__(argv)

        # Create and display the splash screen
        self.splash = SplashScreen()
        self.splash.show()
        self.processEvents()
        __import__("ui.gen.lang_rc")
        self.load_translations(":/lang")

        # Create main window
        self.main = CollectorUI()

        # Show main window
        self.main.show()

        # Hide splash
        self.splash.finish(self.main)

        # Bring window to front
        self.main.raise_()

    # The language code selector is from:
    # switch translations dynamically in a PyQt4 application
    #
    # PyQt version by Hans-Peter Jansen <hpj@urpla.net>

    def load_translations(self, folder):
        """Loads the transaltions from the parameter folder, the translations
         must match the pattern *_*.qm"""
        if not isinstance(folder, QtCore.QDir):
            folder = QtCore.QDir(folder)
        pattern = "*_*.qm"  # <language>_<country>.qm
        filters = QtCore.QDir.Files | QtCore.QDir.Readable
        sort = QtCore.QDir.SortFlags(QtCore.QDir.Name)
        for lang_file in folder.entryInfoList([pattern], filters, sort):
            # pick country and language out of the file name
            language, country = lang_file.baseName().split("_", 1)
            language = language.toLower()
            country = country.toUpper()
            locale = language + "_" + country
            # only load translation, if it does not exist already
            if not locale in CollectorApplication.translators:
                # create and load translator
                translator = QtCore.QTranslator(self.instance())
                if translator.load(lang_file.absoluteFilePath()):
                    CollectorApplication.translators[locale] = translator

        system = QtCore.QLocale.system()

        for lang in CollectorApplication.available_languages():
            if str(lang) == system.name():
                # language match the current system
                CollectorApplication.set_language(lang)

    @staticmethod
    def available_languages():
        """ Returns the avaible languages (code_country) as a list"""
        return sorted(CollectorApplication.translators.keys())

    @staticmethod
    def set_language(locale):
        """ Sets the language of the application using the deseired locale"""
        app = CollectorApplication
        if app.current:
            app.removeTranslator(app.current)
        app.current = app.translators.get(locale, None)
        if app.current is not None:
            app.installTranslator(app.current)


def main():
    """ Starts the application"""
    app = CollectorApplication(sys.argv)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
