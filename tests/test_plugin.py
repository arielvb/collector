# -*- coding: utf-8 -*-

import unittest
import os
from engine.plugin import PluginManager


class TestPluginManager(unittest.TestCase):

    def setUp(self):
        self.manager = PluginManager(
            ['PluginHello'],
            {'PluginHello': 'mocked plugin'})

    def test_disable_not_a_list(self):
        self.assertRaises(TypeError, self.manager.disable, 'PluginHello')

    def test_enable_not_a_list(self):
        self.assertRaises(TypeError, self.manager.enable, 'PluginHello')

    def test_boot_enabled(self):
        self.assertTrue('PluginHello' in self.manager.getEnabled())

    def test_disable_item(self):
        self.manager.disable(['PluginHello'])
        self.assertFalse('PluginHello' in self.manager.getEnabled())

    def test_enable_item(self):
        self.manager.disable(['PluginHello'])
        self.assertFalse('PluginHello' in self.manager.getEnabled())
        self.manager.enable(['PluginHello'])
        self.assertTrue('PluginHello' in self.manager.getEnabled())

    def test_load_enabled_and_run(self):
        path = os.path.join(os.path.dirname(__file__),
                                   'data', 'plugins')
        self.manager.look_for_plugins([path])
        execution_result = self.manager.get('PluginHello').results
        self.assertEqual(execution_result, 'Hello world')

if __name__ == '__main__':
    unittest.main()
