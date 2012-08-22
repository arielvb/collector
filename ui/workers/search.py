# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from engine.search import bgg


class Worker_Search(QtCore.QThread):

    searchComplete = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.results = {}

    def search(self, text):
        #log.debug('Searching...')
        self.action = 'search'
        self.params = {'query': text}
        self.start()

    def run(self):
        self.error = None
        if self.action == 'search':
            self.results['search'] = []
            try:
                p = bgg.search(self.params['query'], bgg.bgg_search_provider, bgg.bgg_search_filter)
                self.results['search'] = p
            except:
                #TODO añadir gestión de errores
                self.error = 'Oopss'
            self.searchComplete.emit()

            return
        if self.action == 'lastgames':
            self.results['lastgames'] = []
            return

    def getLastResult(self):
        return self.results

    def __del__(self):
        self.wait()
