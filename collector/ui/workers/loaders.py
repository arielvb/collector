"""
Loaders
=======

Workers to load files from disk.
"""

from Queue import Queue
from PyQt4 import QtGui, QtCore
import logging


class WorkerImageLoader(QtCore.QThread):
    """
    WorkerImageLoader
    =================
    Worker to defered load images from local files.

    All the images will be scaled afther load using the x and y parameters.
    """

    queue = Queue()
    image_ready = QtCore.pyqtSignal(QtGui.QImage, object)

    def __init__(self, x, y, parent=None):
        super(WorkerImageLoader, self).__init__(parent)
        self.x = x
        self.y = y

    @staticmethod
    def load(path, params):
        """
        Defered load of the image *path*. After load the
         signal *image_ready* is emited with the image contents
         and the input params.
        """
        WorkerImageLoader.queue.put([path, params])

    def run(self):
        """Load all the images of the queue"""
        while not WorkerImageLoader.queue.empty():
            try:
                i = WorkerImageLoader.queue.get()
                image = QtGui.QImage(QtCore.QString.fromUtf8(i[0]))
                if not image.isNull():
                    image2 = image.scaled(
                        self.x,
                        self.y,
                        QtCore.Qt.KeepAspectRatio)
                    del image
                    self.image_ready.emit(
                        image2, i[1])
            except Exception as e:
                logging.exception(e)
                self.image_ready.emit(i[1], None)
            WorkerImageLoader.queue.task_done()
