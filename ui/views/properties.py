# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.gen.properties import Ui_Properties
from ui.widgetprovider import WidgetProvider


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class PropertiesWidget(QtGui.QWidget, Ui_Properties):
    """Properties widget"""

    def __init__(self, parent=None, flags=None):
        if flags is None:
            flags = QtCore.Qt.WindowFlags(0)
        super(PropertiesWidget, self).__init__(parent, flags)
        # self.collection = self.parent().collection.getName()
        self.collection = self.parent().collection
        self.setupUi()

    def setupUi(self):
        super(PropertiesWidget, self).setupUi(self)
        # Title
        text = self.collection.get_title()
        self.title.setText(_fromUtf8(text))
        # Author
        text = self.collection.get_author()
        self.author.setText(_fromUtf8(text))
        # Description
        text = self.collection.get_description()
        self.description.setPlainText(_fromUtf8(text))
        # Persistence
        text = self.collection.get_persistence()
        self.persistence.setText(_fromUtf8(text))

        QtCore.QObject.connect(
            self.buttonBox,
            QtCore.SIGNAL(_fromUtf8("accepted()")),
            lambda: self.save())

        QtCore.QObject.connect(
            self.buttonBox,
            QtCore.SIGNAL(_fromUtf8("rejected()")),
            lambda: self.parent().display_view('dashboard'))
        # TODO save method


class PropertiesView(WidgetProvider):
    """Properties view"""

    def getWidget(self, params):
        # collection = params['collection']
        return PropertiesWidget(self.parent)
