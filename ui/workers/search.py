# -*- coding: utf-8 -*-
from PyQt4.QtCore import QThread, pyqtSignal
from engine.collector import Collector
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
    """Quick search worker"""

    searchComplete = pyqtSignal(WorkerResult)
    partialResult = pyqtSignal([dict])

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.results = {}
        self.params = None

    def search(self, filter_, collection):
        self.params = {'filter': filter_, 'collection': collection}
        self.start()

    def run(self):
        self.error = None
        collector = Collector.get_instance()
        self.results = collector.filter(self.params['collection'],
                                        [self.params['filter']])
        self.searchComplete.emit(WorkerResult(STATUS_OK, self.results))

    def __del__(self):
        self.wait()


class Worker_Discover(QThread):

    searchComplete = pyqtSignal(WorkerResult)
    partialResult = pyqtSignal([list])

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def search(self, text):
        self.params = {'query': text}
        self.start()

    def run(self):
        collector = Collector.get_instance()
        plugins = collector.get_manager('plugin').filter(PluginCollector)
        logging.debug("Discover using: " + str(plugins))
        # Call discover for all the plugins
        all_results = []
        for plugin in plugins:
            try:
                results = collector.discover(self.params['query'],
                                             plugin)
                self.partialResult.emit(results)
                all_results.extend(results)
            except Exception as e:
                logging.debug(e)
                self.searchComplete.emit(
                    WorkerResult(
                        STATUS_ERROR,
                        msg="Plugin %s has failed" % plugin
                    )
                )
                # TODO continue when a plugin has failed
                return
        # Launch the complete
        self.searchComplete.emit(WorkerResult(STATUS_OK, all_results))


class Worker_FileLoader(QThread):

    load_complete = pyqtSignal(WorkerResult)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def search(self, uri, plugin_id):
        self.uri = uri
        self.plugin_id = plugin_id
        self.start()

    def run(self):

        collector = Collector.get_instance()
        try:
            results = collector.get_plugin_file(
                self.uri,
                self.plugin_id
            )
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

from Queue import Queue


class Worker_Queue(QThread):
    """Worker to control all the Worker_FileLoader"""

    complete = pyqtSignal(list)

    def __init__(self, data, parent=None):
        QThread.__init__(self, parent)
        # MAX_THREAD = 2
        self.queue = Queue()
        self.workers = []
        for i in data:
            self.queue.put(i)
        # for i in range(0, MAX_THREAD):
            # worker = Worker_QueueFileLoader()
            # self.workers.append(worker)
            #TODO connect signals/slots
            # worker.resultready.connect(self.subworker_end)
            # worker.search(data['id'], data['plugin'])

    def run(self):
        """The run function"""
        collector = Collector.get_instance()
        results = []
        while not self.queue.empty():
            i = self.queue.get()
            try:
                file_ = collector.get_plugin_file(
                    i['id'],
                    i['plugin'],
                )
                results.append(file_)
            except Exception as e:
                logging.exception(e)
            self.queue.task_done()
        # q.join()
        self.complete.emit(results)

    def add(self, data):
        """Add data to the queue"""
        for i in data:
            self.queue.put(i)
