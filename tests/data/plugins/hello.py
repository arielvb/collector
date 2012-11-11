# -*- coding: utf-8 -*-
from engine.plugin import PluginRunnable


class PluginHello(PluginRunnable):

    results = ''

    def get_author(self):
        return 'Ariel'

    def get_name(self):
        return 'Hello'

    def run(self):
        self.results = 'Hello world'

    def autorun(self):
        return True

    @property
    def icon(self):
        return ''
