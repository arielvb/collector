#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QVariant', 2)

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import qDebug  # Debug!!!
from ui.gen.mainWindow import Ui_MainWindow
from ui.gen.search_quick import Ui_Dialog as Ui_Dialog_Search
from ui.gen.info_dialog import Ui_Dialog as Ui_Dialog_Info
from ui.views.dashboard import DashboardView
from ui.views.fitxa_edit import FitxaEditView
from ui.views.fitxa import FitxaView
from ui.views.collection import CollectionView
from ui.views.search import SearchView
from ui.views.fitxa_new import FitxaNewView
from ui.views.plugins import PluginsView

import time

from engine.collection import CollectionManager
from engine.plugin import PluginManager
from engine.config import Config
from plugins.boardgamegeek import PluginBoardGameGeek

import sys
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class ToolBarManager():

    def __init__(self, parent):
        self.parent = parent
        toolbars = {}
        self.parent.setUnifiedTitleAndToolBarOnMac(True)
        toolBar = QtGui.QToolBar("Navigation")
        self.parent.addToolBar(toolBar)
        # Notify unified title and toolbar on mac (displays collapse button at
        #  the right corner)
        toolbars['navigation'] = toolBar
        self.dashToolbarAction = QtGui.QAction(
            QtGui.QIcon(':/dashboard.png'),
            "&Dashboard", self.parent, shortcut="Ctrl+D",
            statusTip="View dashboard",
            triggered=lambda: self.parent.displatView('dashboard'))
        toolBar.addAction(self.dashToolbarAction)
        toolBar = QtGui.QToolBar("Edition")
        toolbars['edition'] = toolBar
        self.editToolbarAction = QtGui.QAction(
            QtGui.QIcon(':/edit.png'),
            "&Edit", self.parent, shortcut="Ctrl+E",
            statusTip="Edit",
            triggered=lambda: self.parent.editFitxa())
        # self.editToolbarAction.setEnabled(False)
        toolBar.addAction(self.editToolbarAction)
        self.toolbars = toolbars

    def hiddeToolBar(self, toolbar):
        self.parent.setUnifiedTitleAndToolBarOnMac(False)
        self.parent.removeToolBar(self.toolbars[toolbar])
        self.parent.setUnifiedTitleAndToolBarOnMac(True)

    def showToolBar(self, toolbar):
        self.parent.setUnifiedTitleAndToolBarOnMac(False)
        # TODO why once deleted the toolbar it is destroyed and it's impossiblo
        #  to show again?
        self.parent.addToolBar(self.toolbars[toolbar])
        self.parent.setUnifiedTitleAndToolBarOnMac(True)


class CollectorUI(QtGui.QMainWindow, Ui_MainWindow):

    wasMaximized = False
    collection = None

    def __init__(self, parent=None):
        super(CollectorUI,  self).__init__()
        # TODO remove time sleep, now exists only to see the splash screen
        time.sleep(2)

        sys_plugin_path = Config.getInstance().get_appdata_path()
        sys_plugin_path = os.path.join(sys_plugin_path, 'user_plugins')

        self.plugin_manager = PluginManager(
            ['PluginHellouser', 'PluginBoardgamegeek'],
            {'PluginBoardgamegeek': PluginBoardGameGeek()},
            paths=[sys_plugin_path])

        self.collection = CollectionManager.getInstance()

        self.setupUi(self)
        self.setUnifiedTitleAndToolBarOnMac(True)
        # TODO clean toolbar code?
        # self.createToolbar()
        self.createAbout()
        self.initViews()
        self.displayView('dashboard')
        # Menu actions
        QtCore.QObject.connect(
            self.actionView_Dashboard,
            QtCore.SIGNAL(_fromUtf8("triggered()")),
            lambda: self.displayView('dashboard'))
        QtCore.QObject.connect(
            self.actionQuick_search,
            QtCore.SIGNAL(_fromUtf8("triggered()")),
            self.viewQuickSearch)
        QtCore.QObject.connect(
            self.actionFullscreen,
            QtCore.SIGNAL(_fromUtf8("triggered()")),
            self.switchFullscreen)
        QtCore.QObject.connect(
            self.actionSearch_game,
            QtCore.SIGNAL(_fromUtf8("triggered()")),
            lambda: self.searchResults(''))
        QtCore.QObject.connect(
            self.actionManage_plugins,
            QtCore.SIGNAL(_fromUtf8("triggered()")),
            lambda: self.displayView('plugins'))

    def initViews(self):
        self.views = {
            'dashboard': DashboardView(self),
            'fitxa': FitxaView(self),
            'edit': FitxaEditView(self),
            'collection': CollectionView(self),
            'add': FitxaNewView(self),
            'search': SearchView(self),
            'plugins': PluginsView(self)
        }

    def displayView(self, name, params={}):
        """Launches the requested view by name with their parameters,
         if view doesn't exist throws an exception"""
        if not name in self.views:
            raise Exception('View not found')
        self.views[name].run(params)

    def switchFullscreen(self):
        """Display fullscreen mode if isn't not active or shows the previous
        visualitzation maximized or normal window."""
        fullscreen = self.isFullScreen()
        if not fullscreen:
            self.wasMaximized = False
            if self.isMaximized():
                self.wasMaximized = True
            self.showFullScreen()
        else:
            if self.wasMaximized:
                self.showMaximized()
            else:
                self.showNormal()

    def collectorURICaller(self, uri):
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
        for a in params_encoded:
            if key is None:
                key = a
            else:
                params[str(key)] = str(a)
                key = None
        if params_encoded[0] == 'view':
            self.displayView(params['view'], params)
        else:
            return params

    # def viewDashboard(self):
    #     #dashboardWidget = Ui_Dashboard(self)
    #     #self.setCentralWidget(dashboardWidget)
    #     self.views['dashboard'].run()
    #     #self.toolbarManager.hiddeToolBar('edition')

    def viewQuickSearch(self):
        dialog = QtGui.QDialog()
        ui = Ui_Dialog_Search()
        ui.setupUi(dialog)
        dialog.exec_()
        result = dialog.result()
        if result == 1:
            # Accepted
            self.searchResults(ui.lineEdit.text())

    def viewInfo(self, msg):
        dialog = QtGui.QDialog()
        ui = Ui_Dialog_Info()
        ui.setupUi(dialog)
        ui.lMessage.setText(msg)
        dialog.exec_()

    def managePlugins(self):
        w = QtGui.QWidget()
        ui = Ui_Plugins()
        ui.setupUi(w)
        self.setCentralWidget(w)

    # def viewFitxa(self, item):
    #     fitxaWidget = Ui_Fitxa(item, self)
    #     self.fitxa = item
    #     self.setCentralWidget(fitxaWidget)
    #     #self.toolbarManager.showToolBar('edition')

    # def editFitxa(self, item=None):
    #     if item is None:
    #         item = self.fitxa
    #     ui = Ui_Fitxa_Edit(item, self)
    #     self.setCentralWidget(ui)
    #     #self.toolbarManager.hiddeToolBar('edition')

    def about(self):
        about_msg = _fromUtf8("""collector |kəˈlektər|
noun a person or thing that collects something, in particular.
 - New Oxford dictionary

https://www.ariel.cat
                """)
        QtGui.QMessageBox.about(self, "About Collector", about_msg)

    def createAbout(self):
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.aboutAct = QtGui.QAction(
            "&About",
            self,
            statusTip="Show the application's About box",
            triggered=self.about)
        self.helpMenu.addAction(self.aboutAct)

    def createToolbar(self):
        # TODO better toolbar!
        #self.toolbarManager = ToolBarManager(self)
        qDebug('ToolbarCreated')


class SplashScreen():

    def __init__(self):
        splash_pix = QtGui.QPixmap('./data/collector_splash.png')
        self.splash = QtGui.QSplashScreen(splash_pix,
                                          QtCore.Qt.WindowStaysOnTopHint)
        self.splash.setMask(splash_pix.mask())
        self.splash.show()

    def finish(self, ui):
        self.splash.finish(ui)


class CollectorApplication(QtGui.QApplication):

    def __init__(self, argv):
        super(CollectorApplication, self).__init__(argv)

        # Create and display the splash screen
        self.splash = SplashScreen()
        self.processEvents()

        # Create main window
        self.main = CollectorUI()

        # Show main window
        self.main.show()

        # Hide splash
        self.splash.finish(self.main)

        # Bring window to front
        self.main.raise_()


if __name__ == "__main__":

    app = CollectorApplication(sys.argv)

    sys.exit(app.exec_())
