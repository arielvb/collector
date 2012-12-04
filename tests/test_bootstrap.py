import unittest


class TestBoostrap(unittest.TestCase):

    def test_pyqt4_installed(self):
        name = 'pyqt4 not installed'
        try:
            import PyQt4.QtCore
            name = PyQt4.QtCore.__name__
        except:
            pass
        self.assertEqual('PyQt4.QtCore', name)

    def test_ui_is_generated(self):
        name = 'Ui_MainWindow doesn\'t exists'
        try:
            from collector.ui.gen.mainWindow import Ui_MainWindow
            name = Ui_MainWindow.__name__
        except:
            pass
        self.assertEqual('Ui_MainWindow', name)


if __name__ == '__main__':
    unittest.main()
