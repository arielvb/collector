# -*- coding: utf-8 -*-

from PyQt4.QtGui import QListWidgetItem


class FitxaListItem(QListWidgetItem):

    def __init__(self, id, text):
        super(FitxaListItem, self).__init__(text)
        self.id = id
