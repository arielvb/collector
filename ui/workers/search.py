# -*- coding: utf-8 -*-
from PyQt4.QtCore import QThread, pyqtSignal
from engine.collection import CollectionManager
from engine.collector import Collector
from engine.provider import FileProvider
import logging

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
        man = CollectionManager.get_instance()
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
        provider = None
        provider = FileProvider(
            '/Users/arkow/universidad/pfc/collector/tests/data/bgg/' +
            'geeksearch.php.html')
        # bgg = PluginBoardGameGeek(provider)
        collector = Collector.get_instance()
        # TODO call all the plugins
        plugin = 'PluginBoardGameGeek'
        try:
            results = collector.discover(self.params['query'],
             plugin,
             provider)
            self.searchComplete.emit(WorkerResult(STATUS_OK, results))
        except Exception as e:
            logging.debug(e)
            self.searchComplete.emit(
                WorkerResult(
                    STATUS_ERROR,
                    msg="Plugin %s has failed" % plugin
                    )
                )


class Worker_FileLoader(QThread):

    complete = pyqtSignal(WorkerResult)

    def search(self, uri, plugin_id):
        self.uri = uri
        self.plugin_id = plugin_id
        self.start()

    def run(self):
        # TODO remove this provider
        provider = None
        provider = FileProvider(
            '/Users/arkow/universidad/pfc/collector/tests/data/bgg/' +
            'the-pillars-of-the-earth.html')
        collector = Collector.get_instance()
        try:
            results = collector.get_plugin_file(
                         self.uri,
                         self.plugin_id, provider)
            self.complete.emit(WorkerResult(STATUS_OK, results))
        except Exception as e:
            logging.exception(e)
            self.complete.emit(
                WorkerResult(
                    STATUS_ERROR,
                    msg="Plugin %s file load failed with uri %s" %
                     (self.plugin_id, self.uri)
                    )
                )


