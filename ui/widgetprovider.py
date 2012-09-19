# -*- coding: utf-8 -*-


class WidgetProvider(object):
    """Abstract class for the centralwidget of the ui"""

    CENTRAL_WIDGET = 2
    DIALOG_WIDGET = 3

    mode = CENTRAL_WIDGET

    def __init__(self, parent):
        super(WidgetProvider, self).__init__()
        self.parent = parent

    def run(self, params=[]):
        widget = self.getWidget(params)

        if self.mode == self.CENTRAL_WIDGET:
            self.parent.setCentralWidget(widget)

        if self.mode == self.DIALOG_WIDGET:
            widget.exec_()
            self.after_exec(widget)

    def after_exec(self, widget):
        pass
