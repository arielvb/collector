# -*- coding: utf-8 -*-
# pylint: disable-msg=E1101,W0403,E0611
# E0611: No name 'QtCore' in module 'PyQt4'
# E1101: Module 'PyQt4.QtCore' has no 'SIGNAL' member
"""The GUI Application for Collector using QT"""
from PyQt4 import QtCore, QtGui
from splashscreen import SplashScreen
from engine.collector import Collector
from mainwindow import MainWindow


class CollectorApplication(QtGui.QApplication):
    """The GUI Application for Collector"""

    translators = {}
    current = None
    collector = None

    def __init__(self, argv):
        super(CollectorApplication, self).__init__(argv)

        # Create and display the splash screen
        self.splash = SplashScreen()
        self.splash.show()
        self.processEvents()
        # Launch collector
        self.collector = Collector()
        man = self.collector.get_manager('plugin')

        __import__("ui.gen.lang_rc")
        self.load_translations(":/lang")

        # Create main window
        self.main = MainWindow()

        # Show main window
        self.main.show()

        # Hide splash
        self.splash.finish(self.main)

        # Bring window to front
        self.main.raise_()

        if argv is not None:
            self.parse_args(argv)

    def parse_args(self, argv):
        """Parse argv, the input arguments"""
        if '--view' in argv:
            view = argv[argv.index('--view') + 1]
            self.main.display_view(view)
        elif '--uri' in argv:
            self.main.collector_uri_call(argv[argv.index('--uri') + 1])

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
