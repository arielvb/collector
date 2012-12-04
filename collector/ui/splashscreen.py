# -*- coding: utf-8 -*-
"""Splashscreen definition"""

from PyQt4.QtGui import QPixmap, QSplashScreen
from PyQt4.QtCore import Qt
import time
import collector.ui.gen.splash_rc


class SplashScreen(object):
    """Displays a splash screen until the main window is ready"""

    def __init__(self):
        splash_pix = QPixmap(':/splash.png')
        self.splash = QSplashScreen(splash_pix,
                                          Qt.WindowStaysOnTopHint)
        self.splash.setMask(splash_pix.mask())

    def show(self):
        """Displays the splash screen"""
        self.splash.show()
        self.splash.showMessage('Loading...', Qt.AlignBottom | Qt.AlignHCenter,
                                Qt.white)
        # ensure at least its visible one second
        time.sleep(1)

    def finish(self, window):
        """Hides and destroy the splash screen, ensure the """
        self.splash.finish(window)
