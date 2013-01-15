# -*- coding: utf-8 -*-
"""Custom Qt Items"""
from PyQt4.QtGui import QListWidgetItem, QTableWidgetItem
from fields import ImageWidget


class FitxaListItem(QListWidgetItem):
    """Item with id reference"""
    def __init__(self, id, text):
        super(FitxaListItem, self).__init__(text)
        self.id = id


class ObjectListItem(QListWidgetItem):
    """Item with full object reference"""
    def __init__(self, obj, text):
        super(ObjectListItem, self).__init__(text)
        self.obj = obj


class FitxaTableItem(QTableWidgetItem):
    """Table item with identifier reference"""

    def __init__(self, itemId):
        self.id = itemId
        super(FitxaTableItem, self).__init__()

    def getObjectId(self):
        """Returns the object identifier"""
        return self.id


class FitxaTableImage(ImageWidget):
    """Image Table Widget"""

    def __init__(self, itemId):
        self.id = itemId
        super(FitxaTableImage, self).__init__()

    def getObjectId(self):
        return self.id
