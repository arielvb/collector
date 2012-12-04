import unittest
import sip
sip.setapi('QVariant', 2)
from collector.ui.application import CollectorApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import QCoreApplication
import os
import time
import urllib2

HOME = os.path.join(os.path.dirname(__file__), '..', 'data')


class TestApplication(unittest.TestCase):

    def setUp(self):
        '''Create the GUI'''
        self.app = CollectorApplication(["--home", HOME], True)
        # while QCoreApplication.startingUp():
        #     time.sleep(2)

    def tearDown(self):
        self.app.collector.shutdown()
        self.app.quit()
        CollectorApplication.current = None
        CollectorApplication.collector = None
        CollectorApplication.translators = {}
        # while QCoreApplication.closingDown():
        #     time.sleep(2)
        del self.app

    def test_main_window(self):
        from collector.ui.mainwindow import MainWindow
        assert isinstance(self.app.main, MainWindow)

    def test_discoverview(self):
        action = self.app.main.actionDiscover
        # QTest.mouseClick(action)
        action.trigger()
        # self.app.main.hide()
        assert self.app.main.view == "discover"

    def test_network_is_active(self):
        is_google = False
        try:
            urllib2.urlopen('http://google.com', timeout=200)
            is_google = True
        except:
            self.assertTrue(is_google, "Looks like no internet connection"
                " is avaible.")

if __name__ == '__main__':
    unittest.main()
