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
from ui.gen.plugins import Ui_Form as Ui_Plugins
#from ui.views.dashboard import Ui_Dashboard
from ui.views.dashboard import DashboardView
from ui.views.fitxa_edit import FitxaEditView
from ui.views.fitxa import FitxaView
from ui.views.collection import CollectionView
from ui.views.search import Ui_Search
from engine.collection import CollectionManager


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
        # Notify unified title and toolbar on mac (displays collapse button at the right corner)
        toolbars['navigation'] = toolBar
        self.dashToolbarAction = QtGui.QAction(QtGui.QIcon(':/dashboard.png'),
                "&Dashboard", self.parent, shortcut="Ctrl+D",
                statusTip="View dashboard",
                triggered=lambda: self.parent.displatView('dashboard'))
        toolBar.addAction(self.dashToolbarAction)
        toolBar = QtGui.QToolBar("Edition")
        toolbars['edition'] = toolBar
        self.editToolbarAction = QtGui.QAction(QtGui.QIcon(':/edit.png'),
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
        # TODO why once deleted the toolbar it is destroyed and it's impossiblo to show again?
        self.parent.addToolBar(self.toolbars[toolbar])
        self.parent.setUnifiedTitleAndToolBarOnMac(True)


class Ui_Application(QtGui.QMainWindow, Ui_MainWindow):

    wasMaximized = False
    collection = CollectionManager.getInstance()

    def switchFullscreen(self):
        """Display fullscreen mode if isn't not active or shows the previous visualitzation
        maximized or normal window."""
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

    def displayView(self, name, params={}):
        if not name in self.views:
            raise Exception('View not found')
        self.views[name].run(params)

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
        #TODO obtain response of the dialog

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

    def searchResults(self, text):
        w = QtGui.QWidget()
        ui = Ui_Search()
        ui.setupUi(w, self, {'query': text})
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

    def setupUi(self):
        super(Ui_Application,  self).setupUi(self)
        self.createToolbar()
        self.createAbout()
        self.initViews()
        self.displayView('dashboard')
        # Menu actions
        QtCore.QObject.connect(self.actionView_Dashboard, QtCore.SIGNAL(_fromUtf8("triggered()")), lambda: self.displayView('dashboard'))
        QtCore.QObject.connect(self.actionQuick_search, QtCore.SIGNAL(_fromUtf8("triggered()")), self.viewQuickSearch)
        QtCore.QObject.connect(self.actionFullscreen, QtCore.SIGNAL(_fromUtf8("triggered()")), self.switchFullscreen)
        QtCore.QObject.connect(self.actionSearch_game, QtCore.SIGNAL(_fromUtf8("triggered()")), lambda: self.searchResults(''))
        QtCore.QObject.connect(self.actionManage_plugins, QtCore.SIGNAL(_fromUtf8("triggered()")), self.managePlugins)
        #dashboard.setupUi(dashboardWidget, self.centralwidget)

    def initViews(self):
        self.views = {
            'dashboard': DashboardView(self),
            'fitxa': FitxaView(self),
            'fitxa_edit': FitxaEditView(self),
            'collection': CollectionView(self)
        }

    def about(self):
        QtGui.QMessageBox.about(self, "About Application",
                "<b>Collector</b> manages your collections!")

    def createAbout(self):
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.aboutAct = QtGui.QAction("&About", self,
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
        self.splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        self.splash.setMask(splash_pix.mask())
        self.splash.show()

    def finish(self, ui):
        self.splash.finish(ui)

if __name__ == "__main__":
    import sys
    import time
    app = QtGui.QApplication(sys.argv)

    # Create and display the splash screen
    splash = SplashScreen()
    app.processEvents()

    ui = Ui_Application()
    ui.setupUi()
    # TODO remove time sleep, now exists only to see the splash screen
    time.sleep(2)

    # Show window
    ui.show()
    splash.finish(ui)
    # Bring window to front
    ui.raise_()
    sys.exit(app.exec_())
