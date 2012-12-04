# -*- coding: utf-8 -*-
from collector.core.plugin import PluginRunnable
from PyQt4.Qt import qDebug


class PluginHellouser(PluginRunnable):

    def get_author(self):
        return 'Ariel'

    def get_name(self):
        return 'Hello User'

    def run(self):
        qDebug("Hello user!")

    def autorun(self):
        return True

    @property
    def icon(self):
        return ':/browser.png'
