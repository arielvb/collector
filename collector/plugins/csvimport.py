#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""Plugin to Import the CSV from Boardgamegeek"""
from boardgamegeek import PluginBoardGameGeek
from collector.core.controller import Collector
from collector.core.plugin import PluginImporter
from collector.core.provider import UrlProvider
from collector.ui.helpers.fields import FileSelector
from PyQt4 import QtCore, QtGui
import csv
import logging
import os


QStringU8 = QtCore.QString.fromUtf8


class CSVFileSelector(QtGui.QDialog):
    """Widget to obtain a CSV File"""

    def __init__(self, parent=None):
        super(CSVFileSelector, self).__init__()

        self.file = None
        self.collection = None

        # Creating ui elements
        self.resize(400, 135)
        self.setWindowTitle(self.tr("Select a CSV"))
        self.setObjectName(QStringU8("CSVFileSelector"))
        self.mainlayout = QtGui.QHBoxLayout(self)
        self.icon = QtGui.QLabel()
        self.icon.setPixmap(QtGui.QPixmap(':/csvbgg.png'))
        self.mainlayout.addWidget(self.icon)

        self.layout = QtGui.QVBoxLayout()
        self.label = QtGui.QLabel(self.tr(
            QStringU8("Select the CSV file to import:")))
        self.layout.addWidget(self.label)
        self.file_selector = FileSelector(self, 'CSV (*.csv)')
        self.layout.addWidget(self.file_selector)
        self.label2 = QtGui.QLabel(self.tr(
            QStringU8("To the folder:")))
        self.layout.addWidget(self.label2)
        self.collections = QtGui.QComboBox()

        self.layout.addWidget(self.collections)
        self.mainlayout.addLayout(self.layout)
        self.options = QtGui.QDialogButtonBox(self)
        self.options.setOrientation(QtCore.Qt.Horizontal)
        self.options.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
                                        QtGui.QDialogButtonBox.Ok)
        self.options.setObjectName(QStringU8("options"))
        self.layout.addWidget(self.options)

        # Add collections to the combo box
        man = Collector.get_instance().get_manager('collection')
        for i in man.collections.values():
            self.collections.addItem(i.get_name(), i.get_id())
        # Connect things
        self.options.rejected.connect(self.reject)
        self.options.accepted.connect(self.accept)

    def accept(self):
        """Saves the file path and accept"""
        self.file = self.file_selector.get_value()
        self.collection = self.collections.itemData(
            self.collections.currentIndex
        )
        if os.path.exists(self.file):
            super(CSVFileSelector, self).accept()
        else:
            self.file = None
            # Launch error message
            QtGui.QMessageBox.warning(
                self,
                self.tr("Collector"),
                self.tr("Please select an existing file."))


class CSVWorker(QtCore.QThread):
    """
    CSVWorker
    ---------
    This worker reads a csv and import the files to the collection.

    Singals
    .......

    ----------- ------------------------------------------
    csvreaded   notifies the complete read of the csv
    error       launched when an error happens
    filecreated emited every time a file is created
    done        emited when the worker has done their job
    ----------- ------------------------------------------
    """

    csvreaded = QtCore.pyqtSignal(int)
    error = QtCore.pyqtSignal(str)
    filecreated = QtCore.pyqtSignal(int)

    bgg_csv_schema = [
        'objectname',
        'objectid',
        'rating',
        'numplays',
        'weight',
        'own',
        'fortrade',
        'want',
        'wanttobuy',
        'wanttoplay',
        'prevowned',
        'preordered',
        'wishlist',
        'wishlistpriority',
        'wishlistcomment',
        'comment',
        'conditiontext',
        'haspartslist',
        'wantpartslist',
        'collid',
        'baverage',
        'average',
        'avgweight',
        'rank',
        'numowned',
        'objecttype',
        'originalname',
        'minplayers',
        'maxplayers',
        'playingtime',
        'yearpublished',
        'bggrecplayers',
        'bggbestplayers',
        'bggrecagerange',
        'bgglanguagedependence',
        'publisherid',
        'imageid',
        'year',
        'language',
        'other',
        'pricepaid',
        'pp_currency',
        'currvalue',
        'cv_currency',
        'acquisitiondate',
        'acquiredfrom',
        'quantity',
        'privatecomment']

    def __init__(self, path, folder):
        QtCore.QThread.__init__(self)
        self.path = path
        self.folder = folder
        self.provider = UrlProvider("http://boardgamegeek.com/boardgame/%s")
        self.plugin = PluginBoardGameGeek()
        self.stopworking = False

    def run(self):
        self.stopworking = False
        #Open file
        reader = csv.reader(open(self.path))
        # Check header and read rows (each row is a collection file)
        if not self.check_first_row(reader):
            self.error.emit(self.tr("The CSV isn't from Boardgamegeek"))
            return
        files = []
        count = 0  # We need the count of rows for the dialog progress
        for row in reader:
            files.append(row)
            count += 1
        # Emit end of the first step (read file)
        self.csvreaded.emit(count)
        # Add the collections files to the deseired collection
        i = 1
        id = self.bgg_csv_schema.index('objectid')
        man = Collector.get_instance()
        for item in files:
            html = self.provider.get(item[id])
            try:
                data = self.plugin.file_filter(html)
                data['originalname'] = data['title']
                data['title'] = unicode(item[0], 'utf-8')
                # TODO collection id must be a parameter
                man.add(data, 'boardgames', 'PluginCsvImport')
                # TODO add user values and csv-only values
                # from PyQt4.Qt import qDebug; qDebug(unicode(data))
            except Exception as e:
                logging.exception(e)
            self.provider.flush()
            self.filecreated.emit(i)
            if self.stopworking:
                return
            i += 1

    def check_first_row(self, reader):
        """Checks that the first row of the CSV matches with a BGG CSV"""
        row = reader.next()
        return row == self.bgg_csv_schema


class CSVProgress(QtGui.QProgressDialog):
    """Dialog to run the import process and show the status"""

    def __init__(self, path, folder):
        super(CSVProgress, self).__init__(
            QtGui.QApplication.translate("Form", "Reading CSV...", None,
                                         QtGui.QApplication.UnicodeUTF8),
            QtGui.QApplication.translate("Form", "Stop import", None,
                                         QtGui.QApplication.UnicodeUTF8),
            0,
            0)
        self.resize(400, 135)
        self.done = False
        self.worker = CSVWorker(path, folder)
        self.worker.csvreaded.connect(self.set_file_count)
        self.worker.filecreated.connect(self.filecreated)
        self.worker.finished.connect(self.finish)
        self.canceled.connect(self.cancel)

        self.count = 0

    def exec_(self):
        self.worker.start()
        super(CSVProgress, self).exec_()

    def set_file_count(self, i):
        """Sets the file count of the progress dialog"""
        self.count = i
        self.setLabelText(self.tr("Importing files") + " (%d, %d)" % (1, i))
        self.setMinimum(0)
        self.setMaximum(i)

    def filecreated(self, i):
        self.setLabelText(self.tr("Importing files") + " (%d, %d)" %
                          (i, self.count))
        self.setValue(i)

    def cancel(self):
        self.worker.stopworking = True
        self.worker.exit()
        super(CSVProgress, self).cancel()

    def finish(self):
        self.done = True
        self.close()


class PluginCsvImport(PluginImporter):
    """Defines the process to import files from a CSV,
     the expected format of the CSV is the export from Boardgamegeek"""

    @property
    def icon(self):
        return u':/csvbgg.png'

    def get_name(self):
        return "Boardgamegeek CSV"

    def get_author(self):
        return "Ariel"

    def run(self):
        #TODO the current collec. must be a parameter of the front controller
        widget = CSVFileSelector()
        widget.exec_()
        if widget.file is not None:
            progress = CSVProgress(
                widget.file,
                widget.collection
            )
            progress.exec_()
