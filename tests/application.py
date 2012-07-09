import unittest
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt



class TestUi(unittest.TestCase):

    def setUp(self):
        '''Create the GUI'''
        self.app = QApplication(sys.argv)

    def test_application(self):
        from main import Ui_Application
        from ui.gen.mainWindow import Ui_MainWindow
        app = Ui_Application()
        app.setupUi()
        self.assertIsInstance(app, Ui_MainWindow)



if __name__ == '__main__':
    unittest.main()
