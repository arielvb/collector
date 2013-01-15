"""AutoComplete Views and Dialogs"""
from PyQt4 import QtGui, QtCore
from collector.ui.views import Dialog
from collector.ui.workers.search import Worker_Discover


class LoadingAlternatives(QtGui.QProgressDialog):
    """LoadingAlternatives Widget, a progress dialog with steroids"""

    def __init__(self, key, parent):
        super(LoadingAlternatives, self).__init__(
            self,
            self.tr("Looking for data"),
            self.tr("Abort"), 0, 0)
        self.progress.canceled.connect(self.abortautocomplete)
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.show()
        self.worker = Worker_Discover()
        self.worker.searchComplete.connect(self.showalternatives)
        self.worker.search(key)

    def showalternatives(self, results):
        """Choose the alternatives to autocomplete"""
        self.progress.hide()
        self.progress = None

    def abortautocomplete(self):
        if self.worker is not None:
            self.worker.terminate()
            self.worker.wait()


class AlternativesView(Dialog):

    def get_widget(self, params):
        key = params['key']
        w = LoadingAlternatives(key, self.parent)
        return w
