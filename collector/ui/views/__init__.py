# -*- coding: utf-8 -*-
"""Various view utils"""
import abc


class ViewNotFound(Exception):
    """Custom exception raised when a view is requested and doesn't exists"""


class View(object):
    """Abstract class for the centralwidget of the ui"""

    __metaclass__ = abc.ABCMeta

    def __init__(self, parent):
        super(View, self).__init__()
        self.parent = parent

    @abc.abstractmethod
    def run(self, params=None):
        """Runs the view"""

    @abc.abstractmethod
    def get_widget(self, params):
        """Creates the widget with the deseired parameters"""


class Page(View):
    """Central view"""

    def run(self, params=None):
        """Runs the view"""
        if params is None:
            params = {}
        widget = self.get_widget(params)
        self.parent.setCentralWidget(widget)


class Dialog(View):
    """Dialog view"""

    def run(self, params=None):
        """Runs the view"""
        if params is None:
            params = {}
        widget = self.get_widget(params)
        widget.exec_()
        self.after_exec(widget)

    def after_exec(self, widget):
        """Called after run the view"""
        pass
