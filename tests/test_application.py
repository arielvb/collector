import unittest
import sys
import sip
sip.setapi('QVariant', 2)
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt


class TestUi(unittest.TestCase):

    def setUp(self):
        '''Create the GUI'''
        self.app = QApplication(sys.argv)

    def tearDown(self):
        del self.app

    def test_application_can_be_created(self):
        from ui.mainwindow import MainWindow
        from ui.gen.mainWindow import Ui_MainWindow
        app = MainWindow()
        self.assertIsInstance(app, Ui_MainWindow)

    # def test_network_is_active(self):
    #     import urllib2
    #     is_google = False
    #     try:
    #         urllib2.urlopen('http://google.com', timeout=200)
    #         is_google = True
    #     except:
    #         self.assertTrue(is_google, "Looks like no internet connection is avaible.")

if __name__ == '__main__':
    unittest.main()