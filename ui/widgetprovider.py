# -*- coding: utf-8 -*-
"""View provider, or widget provider"""
import abc


class WidgetProvider(object):
    """Abstract class for the centralwidget of the ui"""

    __metaclass__ = abc.ABCMeta

    CENTRAL_WIDGET = 2
    DIALOG_WIDGET = 3

    mode = CENTRAL_WIDGET

    def __init__(self, parent):
        super(WidgetProvider, self).__init__()
        self.parent = parent

    def run(self, params=None):
        """Runs the view"""
        if params is None:
            params = {}
        widget = self.get_widget(params)

        if self.mode == self.CENTRAL_WIDGET:
            self.parent.setCentralWidget(widget)

        if self.mode == self.DIALOG_WIDGET:
            widget.exec_()
            self.after_exec(widget)

    @abc.abstractmethod
    def get_widget(self, params):
        """Creates the widget with the deseired parameters"""


    def after_exec(self, widget):
        """Called after execute the widget is is a dialog"""
        pass
