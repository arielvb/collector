# -*- coding: utf-8 -*-
from PyQt4.QtCore import QThread, pyqtSignal
from engine.collector import Collector
from engine.provider import FileProvider
from engine.plugin import PluginCollector
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
        collector = Collector.get_instance()
        # TODO allow user select the quicksearch collection
        self.results = collector.quick_search(self.params['query'],
                                              'boardgames')
        self.searchComplete.emit(WorkerResult(STATUS_OK, self.results))

    def getLastResult(self):
        return self.results

    def __del__(self):
        self.wait()


class Worker_Discover(QThread):

    searchComplete = pyqtSignal(WorkerResult)
    partialResult = pyqtSignal([dict])

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def search(self, text):
        self.params = {'query': text}
        self.start()

    def run(self):
        # TODO remove this line
        provider = None
        provider = FileProvider(
            '/Users/arkow/universidad/pfc/collector/tests/data/bgg/' +
            'geeksearch.php.html')
        provider = FileProvider(
            '/Users/arkow/munchkinsearch.html')
        collector = Collector.get_instance()
        provider = None

        # TODO call all the plugins
        plugin = 'PluginBoardGameGeek'
        plugins = collector.get_manager('plugin').filter(PluginCollector)
        logging.debug("Discover using: " + str(plugins))
        for plugin in plugins:
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

    load_complete = pyqtSignal(WorkerResult)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def search(self, uri, plugin_id):
        self.uri = uri
        self.plugin_id = plugin_id
        self.start()

    def run(self):
        # TODO remove this provider
        provider = FileProvider(
            '/Users/arkow/universidad/pfc/collector/tests/data/bgg/' +
            'the-pillars-of-the-earth.html')
        provider = None
        collector = Collector.get_instance()
        try:
            results = collector.get_plugin_file(
                         self.uri,
                         self.plugin_id, provider)
            self.load_complete.emit(WorkerResult(STATUS_OK, results))
        except Exception as e:
            logging.exception(e)
            self.load_complete.emit(
                WorkerResult(
                    STATUS_ERROR,
                    msg="Plugin %s file load failed with uri %s" %
                     (self.plugin_id, self.uri)
                    )
                )


