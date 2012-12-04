# -*- coding: utf-8 -*-
# pylint: disable-msg=E1101,W0403,E0611
# E0611: No name 'QtCore' in module 'PyQt4'
# E1101: Module 'PyQt4.QtCore' has no 'SIGNAL' member
"""The GUI Application for Collector using QT"""
from PyQt4 import QtCore, QtGui
from splashscreen import SplashScreen
from collector.core.controller import Collector
import os
import collector.ui.gen.lang_rc
from views.dashboard import DashboardView
from views.fitxa_edit import FitxaEditView
from views.fitxa import FitxaView
from views.collection import CollectionView
from views.search import SearchView, DiscoverView, SearchDialog
from views.fitxa_new import FitxaNewView
from views.preferences import PreferencesView
from views.properties import PropertiesView
from views.plugincollector_fitxa import PluginFileView
from views.advanced_search import AdvancedSearch
from views.im_export import ImportView, ExportView


class CollectorApplication(QtGui.QApplication):
    """The GUI Application for Collector"""

    translators = {}
    current = None
    collector = None

    def __init__(self, argv, hidden=False):
        super(CollectorApplication, self).__init__(argv)

        # Create and display the splash screen
        if not hidden:
            self.splash = SplashScreen()
            self.splash.show()
        self.processEvents()
        self.view = None
        self.uri = None
        self.home = None
        if argv is not None:
            self.parse_args(argv)
        # Launch collector
        self.collector = Collector(self.home)

        self.load_translations(":/lang")

        # Create the main window
        # FIXME: Some view variables are language dependent,
        # is needed to import them after load the language settings
        from mainwindow import MainWindow

        self.main = MainWindow()
        self.main.views = CollectorApplication.get_views(self.main)
        self.main.display_view('dashboard')

        if not hidden:
            # Show main window
            self.main.show()
            # Hide splash
            self.splash.finish(self.main)

        # Bring window to front if development
        if 'COLLECTION_PATH' in os.environ:
            self.main.raise_()

        if self.view is not None:
            self.main.display_view(self.view)
        elif self.uri is not None:
            self.main.collector_uri_call(self.uri)

    def parse_args(self, argv):
        """Parse argv, the input arguments"""
        if '--view' in argv:
            self.view = argv[argv.index('--view') + 1]
        elif '--uri' in argv:
            self.uri = argv[argv.index('--uri') + 1]
        if '--home' in argv:
            self.home = self._checkhome(argv[argv.index('--home') + 1])
        elif '-h' in argv:
            self.home = self._checkhome(argv[argv.index('-h') + 1])

    def _checkhome(self, value):
        """Checks the home value"""
        truehome = os.path.realpath(value)
        if truehome is None:
            raise Exception("Wrong home folder")
            self.quit()
        return truehome

    # The language code selector is from:
    # "switch translations dynamically in a PyQt4 application"
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
        # Get user language from collector.conf
        user_language = self.collector.conf('lang')
        # if user_language is ':system:' or is empty, use the system language
        if user_language in [':system:', '']:
            user_language = system.name()
        # Look if the user_language exists, then set as current language
        for lang in CollectorApplication.available_languages():
            if str(lang) == user_language:
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
            qt_qm = app.translators.get('qt' + locale[2:], None)
            if qt_qm is not None:
                app.installTranslator(qt_qm)

    @staticmethod
    def get_views(parent):
        """ Initialize the avaible views, each view is loaded by a provider"""
        return {
            'dashboard': DashboardView(parent),
            'fitxa': FitxaView(parent),
            'edit': FitxaEditView(parent),
            'collection': CollectionView(parent),
            'add': FitxaNewView(parent),
            'search': SearchView(parent),
            'discover': DiscoverView(parent),
            'preferences': PreferencesView(parent),
            'quicksearch': SearchDialog(parent),
            'properties': PropertiesView(parent),
            'pluginfile': PluginFileView(parent),
            'filters': AdvancedSearch(parent),
            'import': ImportView(parent),
            'export': ExportView(parent),
        }
