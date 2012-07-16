import unittest
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt


class TestUi(unittest.TestCase):

    def setUp(self):
        '''Create the GUI'''
        self.app = QApplication(sys.argv)

    def tearDown(self):
        del self.app

    def test_application(self):
        from main import Ui_Application
        from ui.gen.mainWindow import Ui_MainWindow
        app = Ui_Application()
        app.setupUi()
        self.assertIsInstance(app, Ui_MainWindow)

    def test_network(self):
        import urllib2
        is_google = False
        try:
            urllib2.open('http://google.es', 2)
            is_google = True
        except:
            self.assertTrue(is_google, "Looks that no intenet connection is avaible")

if __name__ == '__main__':
    unittest.main()
