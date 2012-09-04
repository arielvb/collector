# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from engine.search import bgg
from engine.collection import CollectionManager


class Worker_Search(QtCore.QThread):

    searchComplete = QtCore.pyqtSignal()
    action = ''

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.results = {}

    def searchPlugin(self, text):
        self.action = 'searchPlugin'
        self.params = {'query': text}
        self.start()

    def search(self, text):
        self.action = 'search'
        self.params = {'query': text}
        self.start()

    def run(self):
        self.error = None
        if self.action == 'searchPlugin':
            self.results['search'] = []
            try:
                p = bgg.search(self.params['query'], bgg.bgg_search_provider, bgg.bgg_search_filter)
                self.results['searchPlugins'] = p
            except:
                #TODO añadir gestión de errores
                self.error = 'Oopss'
            self.searchComplete.emit()

            return
        if self.action == 'search':
            collection = CollectionManager.getInstance().getCollection('boardgames')
            self.results['search'] = collection.query(self.params['query'])
            self.searchComplete.emit()
            return

    def getLastResult(self):
        return self.results

    def __del__(self):
        self.wait()
