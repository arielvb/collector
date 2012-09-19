# -*- coding: utf-8 -*-
from PyQt4.QtCore import QThread, pyqtSignal
from plugins.boardgamegeek import PluginBoardGameGeek
from engine.collection import CollectionManager

from engine.provider import FileProvider

STATUS_OK = 0
STATUS_ERROR = -1


class WorkerResult(object):

    def __init__(self, status, results=None, msg=""):
        super(WorkerResult, self).__init__()
        self.status = status
        self.results = results
        self.msg = msg


class Worker_Search(QThread):

    searchComplete = pyqtSignal(WorkerResult)
    partialResult = pyqtSignal([dict])

    action = ''

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.results = {}

    def search(self, text):
        self.action = 'search'
        self.params = {'query': text}
        self.start()

    def run(self):
        self.error = None
        man = CollectionManager.getInstance()
        collection = man.getCollection('boardgames')
        self.results = collection.query(self.params['query'])
        self.searchComplete.emit(WorkerResult(STATUS_OK, self.results))

    def getLastResult(self):
        return self.results

    def __del__(self):
        self.wait()


class Worker_Discover(QThread):

    searchComplete = pyqtSignal(WorkerResult)
    partialResult = pyqtSignal([dict])

    def search(self, text):
        self.params = {'query': text}
        self.start()

    def run(self):
        # TODO remove this line
        # FileProvider(
        #     '/Users/arkow/universidad/pfc/collector/tests/data/bgg/' +
        #     'geeksearch.php.html')
        bgg = PluginBoardGameGeek()
        try:
            p = bgg.search(self.params['query'])
            self.searchComplete.emit(WorkerResult(STATUS_OK, p))
        except:
            #TODO añadir gestión de errores
            self.searchComplete.emit(WorkerResult(STATUS_ERROR, msg=""))
