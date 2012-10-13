# -*- coding: utf-8 -*-

from PyQt4.QtGui import QListWidgetItem, QTableWidgetItem


class FitxaListItem(QListWidgetItem):

    def __init__(self, id, text):
        super(FitxaListItem, self).__init__(text)
        self.id = id


class ObjectListItem(QListWidgetItem):

    def __init__(self, obj, text):
        super(ObjectListItem, self).__init__(text)
        self.obj = obj


class FitxaTableItem(QTableWidgetItem):

    def __init__(self, itemId):
        self.id = itemId
        super(FitxaTableItem, self).__init__()

    def getObjectId(self):
        return self.id
